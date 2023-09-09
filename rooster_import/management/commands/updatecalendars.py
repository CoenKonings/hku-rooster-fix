from django.core.management.base import BaseCommand, CommandError
from rooster_import.models import Calendar
from ._calendar_helpers import get_calendar_feed


class Command(BaseCommand):
    help = "Downloads the calendar for year 2 and uses it to update the database."

    def handle(self, *args, **options):
        self.stdout.write("Downloading calendar files...")
        calendars = Calendar.objects.all()

        for calendar in calendars:
            get_calendar_feed(calendar.name, calendar.url)

        self.stdout.write("Done!")
