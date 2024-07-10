import os
import tempfile
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.decorators import login_required
from .models import Submission, Evaluation

# Create your views here.

class UploadForm(forms.Form):
    file = forms.FileField()

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "uploads/"))
if  not out_dir.endswith("/"):
    out_dir += "/"
os.makedirs(out_dir, exist_ok=True)

@login_required
def upload(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            _, filepath = tempfile.mkstemp(prefix=out_dir)
            with open(filepath, "wb") as f:
                f.write(request.FILES["file"].read())
            s = Submission(
                user=request.user,
                status=Submission.Status.UPLOADED,
                data_uri=f"file:///{filepath}"
            )
            s.save()
            e = Evaluation(
                submission=s,
            )
            e.save()
            return HttpResponseRedirect("results")
    else:
        form = UploadForm()
    return render(request, "upload.html", {"form": form})

def results(request: HttpRequest) -> HttpResponse:
    evaluations = Evaluation.objects.all()
    # FIXME: This should be configurable
    RESULT_KEYS = ["lines", "chars"]
    HEADERS = ["username", "status", "last updated"] + RESULT_KEYS
    results = []

    for ev in evaluations:
        row = [ev.submission.user.username, ev.status, ev.last_updated.isoformat()]
        if ev.result:
            for r in RESULT_KEYS:
                row.append(ev.result.get(r, ""))

        results.append(row)
    return render(request, "results.html", {"results": results, "headers": HEADERS})