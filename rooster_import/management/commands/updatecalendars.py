from django.core.management.base import BaseCommand, CommandError
from rooster_import.models import CalendarSource, Event
from ._calendar_helpers import get_calendar_feed, calendar_to_database


class Command(BaseCommand):
    help = "Download ics files and update database to incorporate changes."

    def handle(self, *args, **options):
        calendars = CalendarSource.objects.all()
        # Remove all events to replace them later.
        self.stdout.write("Deleting events...")
        Event.objects.all().delete()

        for calendar in calendars:
            self.stdout.write("Adding {} to database...".format(calendar.name))
            calendar_to_database(calendar.name)

        # TODO: Update ical files for group combinations

        self.stdout.write("Done!")
