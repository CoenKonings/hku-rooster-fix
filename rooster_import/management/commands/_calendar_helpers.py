import requests
import os
from hku_rooster_fix.settings import BASE_DIR


def get_calendar_feed(calendar_name, url):
    """
    Download ICS file containing all events for all groups of all tracks.
    """
    r = requests.get(url)

    if not os.path.isdir(os.path.join(BASE_DIR, "rooster_import", "calendars")):
        os.mkdir(os.path.join(BASE_DIR, "rooster_import", "calendars"))

    open(os.path.join(BASE_DIR, "rooster_import", "calendars", calendar_name + ".ics"), "wb").write(r.content)
