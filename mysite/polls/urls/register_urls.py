from django.urls import path
from django.urls import include, path

from .. import views

urlpatterns = [
    path("", views.register_client, name="register"),
]