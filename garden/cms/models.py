
from django.db import models


class IdentityTitleMeta(models.Model):

    title = models.CharField(max_length=512, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class IdentityNameMeta(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

STATES_CMS = [
    ("delete", "Object is deleted"),
    ("draft", "Object pending to be publish"),
    ("publish", "Object was published"),
]


class StateMeta(models.Model):
    is_publish = models.BooleanField(default=False, blank=False, null=False)
    is_deleted = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        abstract = True

    @property
    def state(self):
        """ Return tuple with key/message"""
        if self.is_deleted:
            return STATES_CMS[0]
        elif self.is_publish:
            return STATES_CMS[2]
        else:
            return STATES_CMS[1]

    def safe_delete(self):
        """Safe delete a model instance"""
        self.is_deleted = True
        self.save()

    def safe_restore(self):
        """Safe delete a model instance"""
        self.is_deleted = False
        self.save()


class TimeElementMeta(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class RevisionElementMeta(models.Model):
    class Meta:
        abstract = True

    rev = models.PositiveIntegerField(default=0)


class ElementMeta(IdentityTitleMeta, StateMeta, RevisionElementMeta, TimeElementMeta):
    class Meta:
        abstract = True

    def __str__(self):
        return f"[{self.rev}] {self.title[:25]} is_active: {self.is_active} | is_publish: {self.is_publish}"


class ObjectMeta(IdentityNameMeta, StateMeta, TimeElementMeta):
    class Meta:
        abstract = True

    def __str__(self):
        return f"[{self.rev}] {self.name} is_active: {self.is_active} | is_publish: {self.is_publish}"


class Page(ElementMeta):
    class Meta:
        abstract = False


class Chapter(ElementMeta):
    pages = models.ManyToManyField(to=Page, related_name="chapter")

    class Meta:
        abstract = False


class Picture(ObjectMeta):

    class Meta:
        abstract = False


class Document(ObjectMeta):

    class Meta:
        abstract = False


class Link(ObjectMeta):

    class Meta:
        abstract = False
