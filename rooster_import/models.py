from django.db import models
from django.conf import settings
from django.conf.urls.static import static
from django.db.models import Q
import icalendar
import os


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
    courses = models.ManyToManyField(Course)
    groups = models.ManyToManyField(Group)

    def get_ical_filename(self):
        """
        Generate the name of the ical file associated with this calendar.
        """
        courses = self.courses.order_by("id")
        groups = self.groups.order_by("id")
        ical_name = "C_"

        for course in courses:
            ical_name += str(course.id) + "_"

        ical_name += "G_"

        for group in groups:
            ical_name += str(group.id) + "_"

        return ical_name + ".ical"

    def generate(self):
        """
        Generate an ical file for this calendar. If one was already made,
        replace it.
        """
        events = []
        courses = self.courses
        groups = self.groups.all()

        for group in groups:
            courses = courses.filter(~Q(group=group))
            events += [event for event in group.event_set.all()]

        if not groups:
            courses = courses.all()

        for course in courses:
            events += [event for event in course.event_set.all()]

        ical = icalendar.Calendar()
        ical.add("prodid", "hkurooster.coenkonings.art")
        ical.add("version", "2.0")
        ical.add("method", "PUBLISH")
        ical.add("name", "HKU Rooster Fix")
        ical.add("x-wr-calname", "HKU Rooster Fix")

        for event in events:
            e = icalendar.Event()
            e.add("name", event.description)
            e.add("summary", event.description)
            e.add("comment", "")
            e.add("description", event.description)
            e.add("dtstart", event.start)
            e.add("dtend", event.end)
            e.add("location", event.location)
            ical.add_component(e)

        with open(
            settings.BASE_DIR
            / "rooster_import/static/rooster_import/calendars/"
            / self.get_ical_filename(),
            "wb",
        ) as file:
            file.write(ical.to_ical())

    def get_url(self):
        """
        Return the url that leads to this calendar's ical file.
        """
        return (
            "https://localhost:8000"
            + settings.STATIC_URL
            + "rooster_import/calendars/"
            + self.get_ical_filename()
        )
