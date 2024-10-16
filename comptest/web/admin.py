from allauth.account.decorators import secure_admin_login
from django.contrib import admin
from reversion.admin import VersionAdmin
from solo.admin import SingletonModelAdmin

from .models import (
    ContentFile,
    Evaluation,
    Page,
    Submission,
    SubmissionMetadata,
    Version,
)


@admin.register(Page)
class PageAdmin(VersionAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ContentFile)
class ContentFileAdmin(VersionAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register([Version, Evaluation, Submission])
admin.site.register(SubmissionMetadata, SingletonModelAdmin)

admin.site.login = secure_admin_login(admin.site.login)
