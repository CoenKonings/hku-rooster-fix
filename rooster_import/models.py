from django.db import models


class Event(models.Model):
    description = models.CharField(max_length=255, null=False)
    location = models.charField(max_length=255, null=True)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=True)
