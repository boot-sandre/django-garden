from django.contrib import admin
from django.urls import path, include
from garden.core import views


url_native_patterns = [
    path("admin/", admin.site.urls),
    path("webtest/", views.std_html_endpoint),
    # path("", include("garden.cms.urls")),
]


url_api_patterns = [
    # Ninja api app
    path("", include("garden.core_ninja.urls")),
]

# Set django urlpatterns
urlpatterns = url_native_patterns + url_api_patterns
