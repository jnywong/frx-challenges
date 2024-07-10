from django.urls import path

from . import views

urlpatterns = [
    path("upload", views.upload, name="upload"),
    path("results", views.results, name="results"),
    path("", views.home, name="home")
]