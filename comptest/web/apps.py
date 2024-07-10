from django.apps import AppConfig
from allauth.socialaccount.signals import pre_social_login


def login_signal(request, sociallogin, **kwargs):
    print(request)
    print(sociallogin)

class WebConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "web"

    def ready(self):
        pre_social_login.connect(login_signal)
