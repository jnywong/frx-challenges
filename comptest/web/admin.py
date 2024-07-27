from allauth.account.decorators import secure_admin_login
from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Evaluation, Page, Submission


@admin.register(Page)
class PageAdmin(VersionAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register([Submission, Evaluation])

admin.site.login = secure_admin_login(admin.site.login)
