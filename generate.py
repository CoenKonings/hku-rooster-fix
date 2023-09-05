import requests
import os


def get_calendar_feed():
    """
    Download ICS file containing all events for all groups of all tracks.
    """
    url = 'http://hku.myx.nl/api/InternetCalendar/feed/28189701-a42e-4729-b313-1fae30133dd1/d73d66d3-e95e-45c0-a6f6-a48c5ba0aee9'
    r = requests.get(url)

    if not os.path.isdir('./calendars/'):
        os.mkdir('calendars')

    open('calendars/jaar2-totaal.ics', 'wb').write(r.content)


def main():
    get_calendar_feed()


if __name__ == "__main__":
    main()
