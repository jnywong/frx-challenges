from allauth.account.decorators import secure_admin_login
from django.contrib import admin

from .models import Evaluation, Submission

admin.site.register([Submission, Evaluation])

admin.site.login = secure_admin_login(admin.site.login)
