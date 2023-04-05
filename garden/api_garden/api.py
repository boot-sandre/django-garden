import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError
from ninja.security import django_auth


from garden.api_garden.routers import router as api_garden_router
from garden.cms_ninja.routers import router as cms_router
from garden.cms_user.routers import router as cms_user_router



api_kwargs = {
    "title": "Django CMS Garden  Api",
    "version": "v0.0.1",
    "description": "CMS garden API",
    "auth": django_auth,
    "csrf": True,
    "docs_decorator": staff_member_required,
}
api_garden = NinjaAPI(**api_kwargs)


@api_garden.exception_handler(ValidationError)
def custom_validation_errors(
    request: HttpRequest, exc: ValidationError
) -> HttpResponse:
    """A validator that will fire a 418 and a message \
    if the data is not compliant to the endpoint schema

    Args:
        request (HttpRequest): the Django http request
        exc (Exception): an exception

    Returns:
        HttpResponse: a Django http response
    """
    print(json.dumps(exc.errors, indent=2))
    return api_garden.create_response(request, {"detail": exc.errors}, status=418)


api_garden.add_router("/cms_user/", cms_user_router)
api_garden.add_router("/cms/", cms_router)
api_garden.add_router("/api_garden/", api_garden_router)
