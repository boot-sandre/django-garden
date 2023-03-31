from typing import Dict, List, Union, Literal
from ninja import Router

from garden.cms.models import Page
from garden.cms_ninja.schemas import PageContract

router = Router(tags=["garden_cms"])


@router.get("hello")
def hello(request):
    return "Hello world"


@router.get(
    "/pages/",
    response={
        200: List[PageContract],
    },
)
def list_pages(request):
    return Page.objects.all()


@router.get(
    "/page/{item_id}",
    response={
        200: PageContract,
    },
)
def get_page(request, item_id: int):
    return Page.objects.get(pk=item_id)
