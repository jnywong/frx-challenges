from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin

from ..models import Page


def view(request: HttpRequest, slug: str) -> HttpResponse:
    page = Page.objects.get(slug=slug)

    md = (
        MarkdownIt("commonmark", {"breaks": True, "html": True})
        .use(front_matter_plugin)
        .use(footnote_plugin)
        .enable("table")
    )
    html_content = md.render(page.content)
    return render(request, "page/view.html", {"page": page, "html_content": html_content})

def home(request: HttpRequest) -> HttpResponse:
    page = Page.objects.get(is_home=True)

    md = (
        MarkdownIt("commonmark", {"breaks": True, "html": True})
        .use(front_matter_plugin)
        .use(footnote_plugin)
        .enable("table")
    )
    html_content = md.render(page.content)
    return render(request, "page/view.html", {"page": page, "html_content": html_content})
