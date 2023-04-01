from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import GardenUser

admin.site.register(GardenUser, UserAdmin)
