from allauth.account.views import LoginView
from django.conf import settings
from django.http import HttpResponse


class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if settings.CHALLENGE_STATE != "RUNNING":
            return HttpResponse(
                "Challenge hasn't started, so login is not available", status=400
            )

        return super().dispatch(request, *args, **kwargs)
