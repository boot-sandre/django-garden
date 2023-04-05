from typing import Dict, List, Union, Literal
from ninja import Router

from garden.cms.models import Page
from garden.cms_ninja.schemas import (
    PageEditContract,
    PageIdentifierContract,
    PageFullContract,
)
from django.shortcuts import get_object_or_404

from garden.api_garden.schemas import ResponseContract

router = Router(tags=["cms_ninja"])


@router.get("hello")
def hello(request):
    return "Hello world"


@router.get(
    "/page/full_list",
    response={
        200: List[PageFullContract],
    },
)
def full_list_pages(request):
    return Page.objects.all()


@router.get(
    "/page/list",
    response={
        200: List[PageIdentifierContract],
    },
)
def list_pages(request):
    return Page.objects.all()


@router.get(
    "/page/get/{page_id}",
    response={
        200: PageFullContract,
    },
)
def get_page(request, page_id: int):
    page = get_object_or_404(Page, pk=page_id)
    return page


@router.post(
    "/page/create",
    response={
        200: PageIdentifierContract,
    },
)
def create_page(request, payload: PageEditContract):
    return Page.objects.create(**payload.dict())


@router.post(
    "/page/update/{page_id}",
    response={
        200: PageIdentifierContract,
    },
)
def update_page(request, page_id: int, payload: PageEditContract):
    page_obj = Page.objects.get(pk=page_id)
    update_items = payload.dict()
    update_keys = update_items.keys()
    for key, value in update_items.items():
        setattr(page_obj, key, value)
    page_obj.save(update_fields=update_keys)
    page_obj.refresh_from_db(fields=update_keys)
    return page_obj


@router.delete(
    "/page/safe_delete/{page_id}",
    response={
        200: ResponseContract,
        405: ResponseContract,
    },
)
def safe_delete(request, page_id: int):
    page = get_object_or_404(Page, pk=page_id)
    page.safe_delete()
    return {"success": True, "message": "CMS page was deactivated"}


@router.delete(
    "/page/safe_restore/{page_id}",
    response={
        200: ResponseContract,
        405: ResponseContract,
    },
)
def safe_restore(request, page_id: int):
    page = get_object_or_404(Page, pk=page_id)
    page.safe_restore()
    return {"success": True, "message": "CMS page was restore"}
