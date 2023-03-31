from django.http import HttpResponse, HttpRequest

from ninja import Router


router = Router(tags=["garden_core"])


@router.get("hello")
def hello(request):
    return HttpResponse(content="Hello world")
