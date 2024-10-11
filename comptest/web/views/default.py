import os
import tempfile

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from ..forms import UploadForm
from ..models import Evaluation, Submission, Version


@login_required
def upload(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # FIXME: We are creating the uploads directory on first use if
            # necessary. This may be a security risk, let's verify.
            os.makedirs(settings.SUBMISSIONS_UPLOADS_DIR, exist_ok=True)
            _, filepath = tempfile.mkstemp(prefix=settings.SUBMISSIONS_UPLOADS_DIR)
            with open(filepath, "wb") as f:
                f.write(request.FILES["file"].read())
            s = Version(
                submission=Submission.objects.get(id=id),
                user=request.user,
                status=Version.Status.UPLOADED,
                data_uri=f"file:///{filepath}",
            )
            s.save()
            return redirect("submissions-detail", id)
    else:
        form = UploadForm()
    return render(request, "upload.html", {"form": form, "id": id})


def results(request: HttpRequest) -> HttpResponse:
    evaluations = Evaluation.objects.all()

    evaluations_resp = []

    for ev in evaluations:
        evaluations_resp.append(
            {
                "username": ev.submission.user.username,
                "status": ev.status,
                "last_updated": ev.last_updated.isoformat(),
                "result": ev.result,
            }
        )

    return JsonResponse({"evaluations": evaluations_resp})


def leaderboard(request: HttpRequest) -> HttpResponse:
    if settings.CHALLENGE_STATE != "RUNNING":
        return HttpResponse(
            "Challenge hasn't started, so leaderboard is not available", status=400
        )

    return render(request, "results.html")
