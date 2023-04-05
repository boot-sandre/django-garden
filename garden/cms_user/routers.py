from django.http import HttpResponse, HttpRequest
from ninja import Router
from ninja.security import django_auth


router = Router(tags=["cms_user"], auth=django_auth)


@router.get("/logging/test/")
def logging(request: HttpRequest):
    return HttpResponse(content="Hello logging")
