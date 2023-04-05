from django.urls import path

from garden.api_garden.api import api_garden


urlpatterns = [
    path("", api_garden.urls),
]
