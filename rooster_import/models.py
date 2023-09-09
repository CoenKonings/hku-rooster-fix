from django.db import models


class Calendar(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)


class Track(models.Model):
    name = models.CharField(max_length=255, null=False)


class Course(models.Model):
    name = models.CharField(max_length=255, null=False)
    tracks = models.ManyToManyField(Track)


class Group(models.Model):
    name = models.CharField(max_length=255, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)


class Event(models.Model):
    description = models.CharField(max_length=255, null=False)
    location = models.CharField(max_length=255, null=True)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=True)
