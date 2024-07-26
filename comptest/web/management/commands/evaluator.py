import asyncio
import json
import os
import tempfile
from urllib.parse import urlparse

import aiodocker
import aiodocker.containers
import fsspec
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef, Q

from ...models import Evaluation, Submission


class DockerEvaluator:
    # Locally built
    image = "quay.io/yuvipanda/evaluator-harness:latest"

    def __init__(self):
        self.docker = aiodocker.Docker()

    async def start_evaluation(self, input_uri):
        results_dir = tempfile.mkdtemp(
            prefix=settings.UNNAMED_THINGY_EVALUATOR_OUTPUTS_TEMPDIR
        )
        results_file = os.path.join(results_dir, "output.json")
        results_uri = f"file://{results_file}"

        url_parts = urlparse(input_uri)
        assert url_parts.scheme == "file"
        input_container_path = "/input"
        output_container_path = "/output"
        container = await self.docker.containers.create(
            config={
                "Image": self.image,
                "Cmd": [
                    f"file://{input_container_path}",
                    f"file://{output_container_path}/output.json",
                ],
                "HostConfig": {
                    "Binds": [
                        # FIXME: This is security critical code, pay attention and
                        # carefully reason about this before deploying to 'production'
                        f"{url_parts.path}:{input_container_path}:ro",
                        f"{results_dir}:{output_container_path}:rw",
                    ]
                },
            }
        )
        await container.start()
        return {
            "container_id": container.id,
            "results_uri": results_uri,
        }

    async def is_still_running(self, state: dict) -> bool:
        container = await self.docker.containers.get(container_id=state["container_id"])
        return container["State"].get("Status") == "running"

    async def get_result(self, state: dict) -> dict:
        container = await self.docker.containers.get(container_id=state["container_id"])
        success = (
            container["State"]["Status"] == "exited"
            and container["State"]["ExitCode"] == 0
        )
        if not success:
            return None
        with fsspec.open(state["results_uri"]) as f:
            result = json.load(f)
        # FIXME: Remove the results file here somehow
        # os.remove(results_file)
        return result


class Command(BaseCommand):
    async def start_evaluation(
        self, evaluator: DockerEvaluator, evaluation: Evaluation
    ):
        print(f"starting evaluation of {evaluation.submission.data_uri}")
        new_state = await evaluator.start_evaluation(evaluation.submission.data_uri)
        evaluation.evaluator_state = new_state
        evaluation.status = Evaluation.Status.EVALUATING
        await evaluation.asave()

    async def process_running_evaluation(
        self, evaluator: DockerEvaluator, evaluation: Evaluation
    ):
        state = evaluation.evaluator_state
        is_still_running = await evaluator.is_still_running(state)
        if not is_still_running:
            print(f"{evaluation} is completed")
            result = await evaluator.get_result(state)
            if result is None:
                evaluation.status = Evaluation.Status.FAILED
            else:
                evaluation.status = Evaluation.Status.EVALUATED
                evaluation.result = result
            await evaluation.asave()
        else:
            print(f"{evaluation} is still running")

    async def ahandle(self):
        evaluator = DockerEvaluator()
        while True:
            # Create evaluation objects when they do not exist
            submissions_without_evaluations = Submission.objects.filter(
                Q(status=Submission.Status.UPLOADED),
                ~Exists(Evaluation.objects.filter(submission=OuterRef("pk"))),
            )
            async for s in submissions_without_evaluations:
                e = Evaluation(submission=s)
                await e.asave()

            # Start Evaluations when they have not been started yet
            unstarted_evaluations = Evaluation.objects.select_related(
                "submission"
            ).filter(status=Evaluation.Status.NOT_STARTED)

            async for e in unstarted_evaluations:
                await self.start_evaluation(evaluator, e)

            # Check running evaluations
            running_evaluations = Evaluation.objects.select_related(
                "submission"
            ).filter(status=Evaluation.Status.EVALUATING)

            async for e in running_evaluations:
                await self.process_running_evaluation(evaluator, e)

            await asyncio.sleep(10)

    def handle(self, *args, **kwargs):
        asyncio.run(self.ahandle())
