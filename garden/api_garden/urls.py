from django.urls import path

from .api import api


urlpatterns = [
    path("api_garden/", api.urls),
]
