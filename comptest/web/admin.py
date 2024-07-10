from django.contrib import admin
from .models import Submission, Evaluation
from allauth.account.decorators import secure_admin_login

admin.site.register([Submission, Evaluation])

admin.site.login = secure_admin_login(admin.site.login)