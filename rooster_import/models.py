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


class Lecturer(models.Model):
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

    def get_lecturers(self):
        lecturers = []

        for event in self.event_set.all():
            for lecturer in event.lecturers.all():
                if lecturer not in lecturers:
                    lecturers.append(lecturer)

        return lecturers


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
    lecturers = models.ManyToManyField(Lecturer)


class Calendar(models.Model):
    groups = models.ManyToManyField(Group)

    def get_ical_filename(self):
        """
        Generate the name of the ical file associated with this calendar.
        """
        course_lecturer_selections = self.courselecturerselection_set.order_by("id")
        groups = self.groups.order_by("id")
        ical_name = "C_"

        for course_lecturers in course_lecturer_selections:
            ical_name += str(course_lecturers.course.id)

            if course_lecturers.lecturers.exists():
                ical_name += "-"

                for lecturer in course_lecturers.lecturers.all():
                    ical_name += str(lecturer.id) + ";"

            ical_name += "_"

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

        courses_lecturers = self.courselecturerselection_set.all()

        for course_lecturers in courses_lecturers:
            course = course_lecturers.course
            groups = self.groups.filter(course=course_lecturers.course)
            lecturers = course_lecturers.lecturers.all()

            print("=============================================")
            print(course_lecturers)
            print(groups)
            print("---------------------------------------------")

            course_events = Event.objects.filter(course=course)

            print(course_events)

            if lecturers:
                course_events = course_events.filter(lecturers__in=lecturers)

            if groups:
                course_events = course_events.filter(group__in=groups)

            events += [event for event in course_events]

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


class CourseLecturerSelection(models.Model):
    """
    This model is necessary to allow users to select specific lecturers whose
    classes they want to import for a certain course. Note that this is
    different from group selection.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturers = models.ManyToManyField(Lecturer)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "selection {}: course {}, lecturers {}, calendar {}".format(
            self.id,
            self.course,
            self.lecturers.all(),
            self.calendar
        )
