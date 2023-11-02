from django.core.management.base import BaseCommand
from rooster_import.models import Course, Group, Event


class Command(BaseCommand):
    help = "Remove all groups and courses with no events in them."

    def handle(self, *args, **options):
        for group in Group.objects.all():
            if not group.event_set.exists():
                group.delete()

        for course in Course.objects.all():
            if not course.event_set.exists():
                course.delete()

        self.stdout.write("Done!")
