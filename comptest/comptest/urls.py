from django.contrib import admin
from django.urls import include, path
from web.views.socialaccount import CustomLoginView

urlpatterns = [
    path("", include("web.urls")),
    path("admin/", admin.site.urls),
    path("accounts/login/", CustomLoginView.as_view(), name="account_login"),
    path("accounts/", include("allauth.urls")),
]
