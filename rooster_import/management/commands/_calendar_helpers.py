import requests
import os


def get_calendar_feed(calendar_name, url):
    """
    Download ICS file containing all events for all groups of all tracks.
    """
    r = requests.get(url)

    if not os.path.isdir("../../calendars/"):
        os.mkdir("../../calendars")

    open("../../calendars/" + calendar_name, "wb").write(r.content)
