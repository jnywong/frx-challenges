from allauth.account.decorators import secure_admin_login
from django.contrib import admin

from .models import Evaluation, Page, Submission

admin.site.register([Submission, Evaluation, Page])

admin.site.login = secure_admin_login(admin.site.login)
