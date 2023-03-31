from ninja import NinjaAPI

from garden.core_ninja.exceptions import GardenApplicationError
from garden.core_ninja.routers import router as core_router
from garden.cms_ninja.routers import router as cms_router


api_kwargs = dict(
    title="Django CMS Garden  Api", version="v0.0.6", description="CMS garden API"
)


api = NinjaAPI(**api_kwargs)


@api.exception_handler(GardenApplicationError)
def garden_application_error(request, exc: GardenApplicationError):
    resp = api.create_response(
        request,
        {"success": False, "message": exc.message},
        status=exc.status_code,
    )
    return resp


api.add_router("/core/", core_router)
api.add_router("/cms/", cms_router)
