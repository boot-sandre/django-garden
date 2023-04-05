from django.db import models
from django.contrib.auth.models import AbstractUser


class GardenUser(AbstractUser):
    # EMAIL_FIELD = "email"
    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username"]

    email = models.EmailField(
        "email address", blank=False, null=False, unique=True)

    class Meta(AbstractUser.Meta):
        abstract = False
