from django.contrib import admin
from .models import Track, Calendar


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
