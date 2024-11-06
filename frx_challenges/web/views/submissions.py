from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..forms import SubmissionForm
from ..md import MARKDOWN_RENDERER
from ..models import Evaluation, Submission


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
    List all submissions of the current user
    """
    submissions = Submission.objects.filter(user=request.user)
    return render(request, "submission/list.html", {"submissions": submissions})


def detail(request: HttpRequest, id: int) -> HttpResponse:
    """
    Show details of a specific submission, such as versions and evaluations
    """
    try:
        submission = Submission.objects.get(id=id)
    except Submission.DoesNotExist:
        raise Http404("Submission does not exist")
    versions = submission.versions.all()

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
    submission = Submission.objects.get(id=id)

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
        request, "submission/edit.html", {"form": form, "html_content": html_content}
    )


@login_required
def detail_evaluation(request: HttpRequest, id: int) -> HttpResponse:
    """
    View evaluation of a submission version
    """
    evaluation = Evaluation.objects.filter(version__user=request.user, id=id)
    return render(request, "submission/evaluation.html", {"evaluation": evaluation})
