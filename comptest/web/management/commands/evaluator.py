import os
import fsspec
import json
import asyncio
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


class Command(BaseCommand):
    def evaluations_to_process(self):
        return Evaluation.objects.select_related("submission").filter(
            status=Evaluation.Status.NOT_STARTED
        )

    async def evaluate(self, evaluation: Evaluation):
        ev = LocalProcessEvaluator(evaluation.submission.data_uri)
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