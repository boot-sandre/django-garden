from django.contrib import admin
from garden.cms.models import Page, Picture, Document, PlaceHolder, Link


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    pass


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    pass


@admin.register(PlaceHolder)
class PlaceHolderAdmin(admin.ModelAdmin):
    pass
