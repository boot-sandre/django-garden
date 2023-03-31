from ninja import NinjaAPI
from ninja.security import django_auth

from garden.core_ninja.routers import router as core_router
from garden.cms_ninja.routers import router as cms_router


# api_kwargs = {"auth": django_auth, "csrf": True}
api_kwargs = {"csrf": True}

api_kwargs.update(
    dict(title="Django CMS Garden  Api", version="v0.0.6", description="CMS garden API")
)


api = NinjaAPI(**api_kwargs)


api.add_router("/core/", core_router)
api.add_router("/cms/", cms_router)
