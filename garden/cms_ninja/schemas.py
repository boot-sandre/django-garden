from typing import Dict, List, Any

from typing import Union
from ninja import Schema, ModelSchema

from garden.cms.models import Page, Chapter


class PageContract(ModelSchema):
    class Config:
        model = Page
        model_fields = ["title", "description", "content"]


class ChapterContract(ModelSchema):
    class Config:
        model = Chapter
        model_fields = ["title", "description"]
