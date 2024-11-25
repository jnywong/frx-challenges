from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..forms import AddCollaboratorForm
from ..models import Collaborator, Submission, User


@login_required
def list(request: HttpRequest, id: int) -> HttpResponse:
    """
    List all collaborators of the submission.
    """
    collaborator = Collaborator.objects.filter(submission_id=id)
    submission = Submission.objects.get(pk=id)
    is_submission_owner = submission.user == request.user
    return render(
        request,
        "collaborator/list.html",
        {
            "collaborators": collaborator,
            "submission": submission,
            "is_submission_owner": is_submission_owner,
        },
    )


@login_required
def add(request: HttpRequest, id: int) -> HttpResponse:
    """
    Add a collaborator to the submission.
    """
    submission = Submission.objects.get(pk=id)
    is_submission_owner = submission.user == request.user

    if is_submission_owner:
        if request.method == "POST":
            form = AddCollaboratorForm(request.POST, submission_id=id)
            if form.is_valid():
                collaborator = Collaborator()
                collaborator.submission_id = id
                user = User.objects.filter(username=form.cleaned_data["username"]).get()
                collaborator.user = user
                collaborator.is_owner = False
                try:
                    collaborator.save()
                except IntegrityError:
                    raise Http404("Database integrity error.")
                return HttpResponseRedirect(reverse("collaborators-list", args=[id]))
        else:
            form = AddCollaboratorForm(submission_id=id)
        return render(request, "collaborator/add.html", {"form": form, "id": id})
    else:
        raise Http404(
            "You are not the submission owner; you are not allowed to add a collaborator to this submission."
        )


@login_required
def delete(request: HttpRequest, id: int, collab_id: int) -> HttpResponse:
    """
    Delete collaborator from the submission.
    """

    submission = Submission.objects.get(pk=id)
    is_submission_owner = submission.user == request.user

    if is_submission_owner:
        collaborator = Collaborator.objects.get(pk=collab_id)
        if collaborator.is_owner:
            raise Http404("The owner of the submission cannot be deleted.")
        collaborator.delete()
    else:
        raise Http404(
            "You are not allowed to remove a collaborator from this submission."
        )

    return HttpResponseRedirect(reverse("collaborators-list", args=[id]))
