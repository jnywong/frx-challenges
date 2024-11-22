from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..models import Collaborators, Submission


@login_required
def list(request: HttpRequest, id: int) -> HttpResponse:
    """
    List all collaborators of the submission.
    """
    collaborators = Collaborators.objects.filter(submission_id=id)
    submission = Submission.objects.get(pk=id)
    return render(
        request,
        "collaborators/list.html",
        {"collaborators": collaborators, "submission": submission},
    )
