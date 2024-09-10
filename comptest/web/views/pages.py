from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

from ..models import Page


def view(request: HttpRequest, slug: str) -> HttpResponse:
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        return Http404()

    md = (
        MarkdownIt("commonmark", {"breaks": True, "html": True})
        .use(front_matter_plugin)
        .use(footnote_plugin)
        .enable("table")
    )
    html_content = md.render(page.content)
    return render(
        request, "page/view.html", {"page": page, "html_content": html_content}
    )


def home(request: HttpRequest) -> HttpResponse:
    page = Page.objects.get(is_home=True)

    md = (
        MarkdownIt("commonmark", {"breaks": True, "html": True})
        .use(front_matter_plugin)
        .use(footnote_plugin)
        .enable("table")
    )
    html_content = md.render(page.content)
    context = {
        "page": page,
        "html_content": html_content,
        "challenge_state": settings.CHALLENGE_STATE,
    }
    return render(request, "page/view.html", context)
