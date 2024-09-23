from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

from ..models import ContentFile, Page


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

    if page.mimetype == Page.MimeType.markdown:
        md = (
            MarkdownIt("commonmark", {"breaks": True, "html": True})
            .use(front_matter_plugin)
            .use(footnote_plugin)
            .enable("table")
        )
        html_content = md.render(page.content)
    elif page.mimetype == Page.MimeType.html:
        html_content = page.content
    else:
        raise ValueError(f"Unsupported mimetype {page.mimetype} for {page.title}")

    context = {
        "page": page,
        "html_content": html_content,
        "challenge_state": settings.CHALLENGE_STATE,
    }
    return render(request, "page/view.html", context)


def content_file(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Redirect to file with given slug
    """
    try:
        cf = ContentFile.objects.get(slug=slug)
    except Page.DoesNotExist:
        return Http404()
    return redirect(cf.file.url)
