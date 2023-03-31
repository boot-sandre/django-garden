from django.db import models


class ElementBasicMeta:
    title = models.CharField(max_length=512, blank=False, null=False)
    description = models.TextField(blank=True, null=True)


class StateElementMeta:
    is_publish = models.BooleanField(default=False, blank=False, null=False)
    is_active = models.BooleanField(default=True, blank=False, null=False)


class RevisionElementMeta:
    rev = models.IntegerField(default=0)


class ElementMeta(ElementBasicMeta, StateElementMeta, RevisionElementMeta):
    pass


class Chapter(models.Model, ElementMeta):
    pass


class Page(models.Model, ElementMeta):
    pass
