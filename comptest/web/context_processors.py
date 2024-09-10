from django.conf import settings

from .models import Page


def navbar_pages(request):
    pages = Page.objects.all().order_by("order").exclude(is_home=True)
    return {"pages": pages}


def footer_content(request):
    return {"footer": settings.FOOTER}
