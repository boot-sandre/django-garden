from ninja import NinjaAPI

from garden.api_garden.exceptions import GardenApplicationError

from garden.api_garden.routers import router as api_garden_router
from garden.cms_ninja.routers import router as cms_router
from garden.cms_user.routers import router as cms_user_router


api_kwargs = dict(
    title="Django CMS Garden  Api", version="v0.0.7", description="CMS garden API",
    csrf=True
)
api = NinjaAPI(**api_kwargs)

api.add_router("/cms_user/", cms_user_router)
api.add_router("/cms/", cms_router)
api.add_router("/api_garden/", api_garden_router)


@api.exception_handler(GardenApplicationError)
def garden_application_error(request, exc: GardenApplicationError):
    resp = api.create_response(
        request,
        {"success": False, "message": exc.message},
        status=exc.status_code,
    )
    return resp
