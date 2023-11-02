from django.core.management.base import BaseCommand
from rooster_import.models import CalendarSource, Event, Calendar
from ._calendar_helpers import get_calendar_feed, calendar_to_database


class Command(BaseCommand):
    help = "Download ics files and update database to incorporate changes."

    def handle(self, *args, **options):
        calendar_sources = CalendarSource.objects.all()
        # Remove all events to replace them later.
        self.stdout.write("Deleting events...")
        Event.objects.all().delete()

        for calendar_source in calendar_sources:
            self.stdout.write("Adding {} to database...".format(calendar_source.name))
            get_calendar_feed(calendar_source.name, calendar_source.url)
            calendar_to_database(calendar_source.name)

        self.stdout.write("Updating ical files...")

        for calendar in Calendar.objects.all():
            self.stdout.write("Updating {}".format(calendar.get_ical_filename()))
            calendar.generate()

        self.stdout.write("Done!")
