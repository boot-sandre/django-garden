from typing import Dict, List, Any

from typing import Union
from ninja import Schema, ModelSchema

from garden.cms.models import Page, Chapter


meta_fields = ["is_publish", "is_deleted", "created_at", "updated_at", "rev"]
share_content_fields = ["title", "description"]
page_content_fields = share_content_fields + ["content"]


class PageEditContract(ModelSchema):
    class Config:
        model = Page
        model_fields = page_content_fields


class PageIdentifierContract(ModelSchema):
    class Config(PageEditContract.Config):
        model_fields = ["id"] + page_content_fields


class PageFullContract(ModelSchema):
    class Config(PageEditContract.Config):
        model_fields = ["id"] + page_content_fields + meta_fields


class ChapterDataContract(ModelSchema):
    class Config:
        model = Chapter
        model_fields = share_content_fields


class ChapterContract(ModelSchema):
    class Config:
        model = Chapter
        model_fields = ["id"] + share_content_fields
