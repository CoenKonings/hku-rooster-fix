from django.db import models


class CalendarSource(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url = models.URLField(max_length=255)


class Track(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    tracks = models.ManyToManyField(Track)

    def __str__(self):
        return "Course {}.".format(self.name)

    def track_ids(self):
        return [track.id for track in self.tracks.all()]


class Group(models.Model):
    name = models.CharField(max_length=255, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Event(models.Model):
    description = models.CharField(max_length=255, null=False)
    location = models.CharField(max_length=255, null=True)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)


class Calendar(models.Model):
    tracks = models.ManyToManyField(Track)
    courses = models.ManyToManyField(Course)
