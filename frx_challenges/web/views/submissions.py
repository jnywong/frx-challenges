from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..forms import SubmissionForm
from ..md import MARKDOWN_RENDERER
from ..models import Collaborator, Submission


@login_required
def create(request: HttpRequest) -> HttpResponse:
    """
    Create a new submission.
    """
    html_content = MARKDOWN_RENDERER.render(
        settings.SITE_SUBMISSION_INSTRUCTIONS_MARKDOWN
    )

    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = Submission()
            submission.user = request.user
            submission.name = form.cleaned_data["name"]
            submission.description = form.cleaned_data["description"]
            submission.metadata = form.cleaned_data["metadata"]
            submission.toc_accepted = form.cleaned_data["toc_accepted"]
            submission.save()
            collaborator = Collaborator()
            collaborator.submission_id = submission.id
            collaborator.user_id = request.user.id
            collaborator.is_owner = True
            collaborator.save()
            return HttpResponseRedirect(
                reverse("submissions-detail", args=[submission.id])
            )
    else:
        form = SubmissionForm()

    return render(
        request, "submission/create.html", {"form": form, "html_content": html_content}
    )


@login_required
def list(request: HttpRequest) -> HttpResponse:
    """
    List all submissions of the current user/collaborator.
    """
    collaborator = Collaborator.objects.filter(user=request.user).values_list(
        "submission_id"
    )
    submissions = Submission.objects.filter(id__in=collaborator)
    return render(request, "submission/list.html", {"submissions": submissions})


def detail(request: HttpRequest, id: int) -> HttpResponse:
    """
    Show details of a specific submission, such as versions and evaluations
    """
    try:
        submission = Submission.objects.get(id=id)
    except Submission.DoesNotExist:
        raise Http404("Submission does not exist.")
    is_collaborator = _validate_collaborator(request, id)

    versions = submission.versions.all()

    # Determine if request.user is a submission collaborator
    if request.user == submission.user:
        is_owner = True
    else:
        is_owner = False

    # Decide how we display metadata
    metadata_display = []
    if settings.SITE_SUBMISSION_FORM_SCHEMA:
        for k, v in settings.SITE_SUBMISSION_FORM_SCHEMA["properties"].items():
            if v["type"] == "string":
                metadata_display.append(
                    {
                        "display_name": v["title"],
                        "help_string": v.get("helpText"),
                        "value": submission.metadata.get(k),
                        "format": v.get("format")
                    }
                )
            else:
                raise ValueError(f"Unsupported metadata schema type {v['type']} found")

    return render(
        request,
        "submission/detail.html",
        {
            "submission": submission,
            "versions": versions,
            "metadata_display": metadata_display,
            "is_owner": is_owner,
            "is_collaborator": is_collaborator,
        },
    )


@login_required
def edit(request: HttpRequest, id: int) -> HttpResponse:
    """
    Edit submission metadata
    """

    html_content = MARKDOWN_RENDERER.render(
        settings.SITE_SUBMISSION_INSTRUCTIONS_MARKDOWN
    )

    # Get model instance to pre-populate form
    try:
        submission = Submission.objects.get(id=id)
    except Submission.DoesNotExist:
        raise Http404("Submission does not exist.")

    # Raise error if user is not the owner of the submission
    if request.user != submission.user:
        raise Http404("You are not the owner of this submission.")

    if request.method == "POST":
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            submission.user = request.user
            submission.name = form.cleaned_data["name"]
            submission.description = form.cleaned_data["description"]
            submission.metadata = form.cleaned_data["metadata"]
            submission.toc_accepted = form.cleaned_data["toc_accepted"]
            submission.save()
            return HttpResponseRedirect(
                reverse("submissions-detail", args=[submission.id])
            )
    else:
        form = SubmissionForm(instance=submission)

    return render(
        request,
        "submission/edit.html",
        {"form": form, "html_content": html_content, "submission": submission},
    )


def _validate_collaborator(request: HttpRequest, submission_id: int):
    """
    Check if current user is a collaborator on this submission
    """
    if request.user.is_anonymous:
        return False
    try:
        Collaborator.objects.get(submission_id=submission_id, user=request.user)
        return True
    except Collaborator.DoesNotExist:
        return False
