import os
import aiodocker.containers
import fsspec
import json
import aiodocker
import asyncio
from urllib.parse import urlparse
import tempfile
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q, Exists, OuterRef
from ...models import Evaluation, Submission


class LocalProcessEvaluator:
    harnass_process = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../../harness/longest.py")
        )
    def __init__(self, data_uri: str):
        self.data_uri = data_uri
        _, self.results_file = tempfile.mkstemp()
        self.results_uri = f'file:///{self.results_file}'

    async def start_evaluation(self):
        self.proc = await asyncio.create_subprocess_exec(
            self.harnass_process,
            self.data_uri,
            self.results_uri
        )

    async def wait_for_result(self) -> dict:
        await self.proc.wait()
        if self.proc.returncode != 0:
            # FIXME: Signal failure better
            return None
        with fsspec.open(self.results_uri) as f:
            result = json.load(f)
        os.remove(self.results_file)
        return result




class DockerEvaluator:
    # Locally built
    image = "quay.io/yuvipanda/evaluator-harness:latest"

    def __init__(self, data_uri: str):
        self.data_uri = data_uri
        self.docker = aiodocker.Docker()

        # Make a local directory for containing outputs if needed
        # FIXME: Move this somewhere else or make this configurable
        # This *must* be bind mountable into the docker container
        out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "outputs/"))
        if  not out_dir.endswith("/"):
            out_dir += "/"
        os.makedirs(out_dir, exist_ok=True)

        self.results_dir = tempfile.mkdtemp(prefix=out_dir)
        self.results_file = os.path.join(self.results_dir, "output.json")
        self.results_uri = f'file://{self.results_file}'

    async def start_evaluation(self):
        url_parts = urlparse(self.data_uri)
        assert url_parts.scheme == "file"
        input_container_path = "/input"
        output_container_path = "/output"
        self.container = await self.docker.containers.create(config={
            "Image": self.image,
            "Cmd": [f"file://{input_container_path}", f"file://{output_container_path}/output.json"],
            "HostConfig": {
                "Binds": [
                    # FIXME: This is security critical code, pay attention and
                    # carefully reason about this before deploying to 'production'
                    f"{url_parts.path}:{input_container_path}:ro",
                    f"{self.results_dir}:{output_container_path}:rw"
                ]
            }
        })
        await self.container.start()

    async def wait_for_result(self) -> dict:
        await self.container.wait()
        with fsspec.open(self.results_uri) as f:
            result = json.load(f)
        os.remove(self.results_file)
        return result


class Command(BaseCommand):
    def evaluations_to_process(self):
        return Evaluation.objects.select_related("submission").filter(
            status=Evaluation.Status.NOT_STARTED
        )

    async def evaluate(self, evaluation: Evaluation):
        ev = DockerEvaluator(evaluation.submission.data_uri)
        await ev.start_evaluation()
        evaluation.status = Evaluation.Status.EVALUATING
        await evaluation.asave()
        print(f"starting evaluation of {evaluation.submission.data_uri}")
        result = await ev.wait_for_result()
        if result is None:
            evaluation.status = Evaluation.Status.FAILED
        else:
            evaluation.result = result
            evaluation.status = Evaluation.Status.EVALUATED
        await evaluation.asave()
        print(f'Result is {result}')


    async def ahandle(self):
        while True:
            async for e in self.evaluations_to_process():
                await self.evaluate(e)

            await asyncio.sleep(10)

    def handle(self, *args, **kwargs):
        asyncio.run(self.ahandle())