import os
import tempfile
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
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
            # FIXME: Figure out transactions
            s.save()
            e = Evaluation(
                submission=s,
            )
            e.save()
            return HttpResponseRedirect("/")
    else:
        form = UploadForm()
    return render(request, "upload.html", {"form": form})

def results(request: HttpRequest) -> HttpResponse:
    evaluations = Evaluation.objects.all()

    evaluations_resp = []

    for ev in evaluations:
        evaluations_resp.append({
            "username": ev.submission.user.username,
            "status": ev.status,
            "last_updated": ev.last_updated.isoformat(),
            "result": ev.result
        })

    return JsonResponse({
        "evaluations": evaluations_resp
    })

def home(request: HttpRequest) -> HttpResponse:
    return render(request, "results.html")