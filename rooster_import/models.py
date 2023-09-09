from django.db import models


class Track(models.Model):
    name = models.CharField(max_length=255)


class Course(models.Model):
    name = models.CharField(max_length=255)
    tracks = models.ManyToManyField(Track)


class Group(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course)


class Event(models.Model):
    description = models.CharField(max_length=255, null=False)
    location = models.charField(max_length=255, null=True)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=True)
