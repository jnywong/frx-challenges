from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

from ..forms import SubmissionForm
from ..models import Evaluation, Submission, SubmissionMetadata


@login_required
def create(request: HttpRequest) -> HttpResponse:
    """
    Create a new submission.
    """
    if SubmissionMetadata.objects.exists():
        md = (
            MarkdownIt("commonmark", {"breaks": True, "html": True})
            .use(front_matter_plugin)
            .use(footnote_plugin)
            .enable("table")
        )
        html_content = md.render(SubmissionMetadata.objects.latest().instructions)

    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = Submission()
            submission.user = request.user
            submission.name = form.cleaned_data["name"]
            submission.description = form.cleaned_data["description"]
            if SubmissionMetadata.objects.exists():
                submission.metadata = _serialize_submission_metadata(form)
            submission.save()
            return HttpResponseRedirect("/submissions")
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


@login_required
def detail(request: HttpRequest, id: int) -> HttpResponse:
    """
    Show details of a specific submission, such as versions and evaluations
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
def detail_evaluation(request: HttpRequest, id: int) -> HttpResponse:
    """
    View evaluation of a submission version
    """
    evaluation = Evaluation.objects.filter(version__user=request.user, id=id)
    return render(request, "submission/evaluation.html", {"evaluation": evaluation})


def _serialize_submission_metadata(inputForm):
    """Serializes metadata from submission form into JSON"""
    fields = SubmissionMetadata.objects.latest().items
    values = [inputForm.cleaned_data[f] for f in fields]

    json_dict = {key: value for key, value in zip(fields, values)}

    return json_dict
