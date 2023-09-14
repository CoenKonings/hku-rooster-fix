from django.contrib import admin
from .models import Track, CalendarSource, Course, Group, Event, Calendar


@admin.register(CalendarSource)
class CalendarSourceAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "description", "start", "end"]
