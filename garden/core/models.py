from django.db import models


# Create your models here.
class TimeEvent(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField("Created", auto_now_add=True)
    last_modified = models.DateTimeField("Last Modified", auto_now=True)
