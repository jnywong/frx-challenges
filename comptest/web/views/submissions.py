from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from ..forms import SubmissionForm
from ..models import Evaluation, Submission


@login_required
def create(request: HttpRequest) -> HttpResponse:
    """
    Create a new submission.
    """
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = Submission()
            submission.user = request.user
            submission.name = form.cleaned_data["name"]
            submission.description = form.cleaned_data["description"]
            submission.gh_repo = form.cleaned_data["gh_repo"]
            submission.save()
            return HttpResponseRedirect("/submissions")
    else:
        form = SubmissionForm()

    return render(request, "submission/create.html", {"form": form})


@login_required
def list(request: HttpRequest) -> HttpResponse:
    """
    List all submissions of the current user
    """
    submissions = Submission.objects.filter(user=request.user)
    return render(request, "submission/list.html", {"submissions": submissions})


@login_required
def detail(request: HttpRequest, id: int) -> HttpResponse:
    """
    Show details of a specific submission
    """
    queryset = Submission.objects.filter(
        user=request.user
    )  ## TODO: test that another user cannot access the current user's submission
    submission = queryset.get(id=id)
    versions = submission.version_set.all()
    return render(
        request,
        "submission/detail.html",
        {"submission": submission, "versions": versions},
    )


@login_required
def list_evaluations(request: HttpRequest) -> HttpResponse:
    """
    List all evaluations of the current user
    """
    evaluations = Evaluation.objects.filter(version__user=request.user)
    return render(request, "submissions.html", {"evaluations": evaluations})
