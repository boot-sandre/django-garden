from django.urls import path

from . import views

urlpatterns = [
    path("endpoint/", views.endpoint),
]
