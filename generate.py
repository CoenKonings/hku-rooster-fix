import requests
import os
from icalendar import Calendar, Event


def group_events_by_track(calendar_path):
    """
    Split the calendar for mt2 totaal into one Calendar object for each track.
    """
    with open(calendar_path, 'rb') as calendar_file:
        mt2_totaal = Calendar.from_ical(calendar_file.read())

    cals = {}
    tracks = ['MT2 COMP', 'MT2 KO', 'MT2 CSD', 'MT2 PROD']

    for i in range(len(tracks)):
        cal = Calendar()
        cal.add('prodid', 'hku-rooster-fix-coen-konings')
        cal.add('version', '2.0')
        cals[tracks[i]] = cal

    for c in mt2_totaal.walk():
        if c.name == 'VEVENT':
            attendees = c.get('attendee')
            for attendee in attendees:
                attendee_name = attendee.params['CN']

                if attendee_name in cals.keys():
                    cals[attendee_name].add_component(c)
                elif attendee_name == 'MT jaar 2':
                    for cal in cals.values():
                        cal.add_component(c)

    return cals


def get_calendar_feed(calendar_path):
    """
    Download ICS file containing all events for all groups of all tracks.
    """
    url = 'http://hku.myx.nl/api/InternetCalendar/feed/28189701-a42e-4729-b313-1fae30133dd1/d73d66d3-e95e-45c0-a6f6-a48c5ba0aee9'
    r = requests.get(url)

    if not os.path.isdir('./calendars/'):
        os.mkdir('calendars')

    open(calendar_path, 'wb').write(r.content)


def main():
    mt2_totaal_path = 'calendars/jaar2-totaal.ics'
    get_calendar_feed(mt2_totaal_path)
    track_calendars = group_events_by_track(mt2_totaal_path)

    for cal in track_calendars.values():
        for c in cal.walk():
            if c.name == 'VEVENT':
                print(c.get('description'))
                break


if __name__ == "__main__":
    main()
