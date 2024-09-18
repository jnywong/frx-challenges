from django.contrib import admin
from django.urls import include, path
from web.views.socialaccount import CustomLoginView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", include("web.urls")),
    path("admin/", admin.site.urls),
    path("accounts/login/", CustomLoginView.as_view(), name="account_login"),
    path("accounts/", include("allauth.urls")),
]

# Enable static serving even with external webserver like gunicorn
urlpatterns += staticfiles_urlpatterns()