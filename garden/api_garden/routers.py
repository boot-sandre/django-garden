from django.http import HttpResponse, HttpRequest

from ninja import Router


router = Router(tags=["api_garden"])


@router.get("hello")
def hello(request: HttpRequest):
    return HttpResponse(content="Hello world")
