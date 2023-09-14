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
    courses = models.ManyToManyField(Course)
    groups = models.ManyToManyField(Group)

    def get_ical_filename(self):
        """
        Generate the name of the ical file associated with this calendar.
        """
        courses = self.courses.order_by("id")
        groups = self.groups.order_by("id")
        ical_name = "c_"

        for course in courses:
            ical_name += str(course.id) + "_"

        ical_name += "g_"

        for group in groups:
            ical_name += str(group.id) + "_"

        return ical_name + ".ical"

    def generate(self):
        """
        Generate an ical file for this calendar. If one was already made,
        replace it.
        """

    def get_url(self):
        """
        Return the url that leads to this calendar's ical file.
        """
