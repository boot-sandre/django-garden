from django.db import models
from garden.cms import meta


class Page(meta.ElementMeta):
    content = models.TextField(null=True, blank=True)

    class Meta:
        abstract = False


class Picture(meta.ObjectMeta, meta.FileMeta):
    class Meta:
        abstract = False


class Document(meta.ObjectMeta, meta.FileMeta):
    class Meta:
        abstract = False


class Link(meta.ObjectMeta):
    url = models.URLField(blank=False, null=True)

    class Meta:
        abstract = False


class PlaceHolder(meta.ObjectMeta):
    tag_link = models.CharField(max_length=32, blank=False, null=False)
    content = models.TextField()

    class Meta:
        abstract = False
