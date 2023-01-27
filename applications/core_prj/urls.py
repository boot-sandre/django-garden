from django.urls import path

from . import views

urlpatterns = [
    path("test/", views.std_html_endpoint),
]
