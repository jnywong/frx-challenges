from django.conf import settings

from .models import Page


def navbar_pages(request):
    pages = Page.objects.all().order_by("order").exclude(is_home=True)
    return {"pages": pages}


def site_display_settings(request):
    return {
        "site_name": settings.SITE_NAME,
        "site_logo_url": settings.SITE_LOGO_URL,
        "site_footer_html": settings.SITE_FOOTER_HTML
    }
