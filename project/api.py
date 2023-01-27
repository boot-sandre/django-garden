from ninja import NinjaAPI
from applications.core_prj.routers import router as core_prj_router


api = NinjaAPI()

api.add_router("/core_prj/", core_prj_router)
