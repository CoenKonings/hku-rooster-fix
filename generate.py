import requests
import os
from icalendar import Calendar


def cal_for_all_group_combinations(groups):
    """
    Create a Calendar object for all possible combinations of the given groups.
    Groups should be a dictionary, where each key is a course name and each
    value is another dictionary. This dictionary should contain each group
    number as a key, where the corresponding value is a list of all events for
    that group.
    """
    courses_group_names = {}

    for course_name in groups:
        group_names = []

        for group_name in groups[course_name]:
            group_names.append(group_name)

        courses_group_names[course_name] = group_names

    print(courses_group_names)


def generate_ical_files(track_calendars):
    """
    Generate ical files for all possible track and group combinations.
    """
    for track_name in track_calendars:
        track_calendar = track_calendars[track_name]
        everyone, groups = split_course_groups(track_calendar)
        group_cals = cal_for_all_group_combinations(groups)


def calendar_from_groups(groups):
    """
    Generate a calendar for the given groups. The groups parameter should
    contain a dictionary where the group names are the keys, and the events are
    their values.
    """
    calendar = Calendar()
    calendar.add('prodid', 'hku-rooster-fix-coen-konings')
    calendar.add('version', '2.0')

    for group in groups:
        events = groups[group]

        for event in events:
            calendar.add_component(event)

    return calendar


def groups_from_event_name(name):
    """
    Find the group numbers and course name from an event name.
    """
    groups = []
    course_name = ''

    for word in name.split(' '):
        if word.lower() == 'groep' or word.lower() == 'en':
            continue
        elif word.isnumeric():
            groups.append(word)
        else:
            course_name += word + ' '

    return course_name.strip(), groups


def split_course_groups(calendar):
    """
    Find out which groups exist for each course in this calendar. Create a
    dictionary containing all events for each group.
    """
    course_groups = {}
    everyone = []

    for c in calendar.walk():
        if c.name == 'VEVENT':
            if 'groep' in c.get('summary').lower() and 'hele groep' not in c.get('summary').lower():
                course, groups = groups_from_event_name(c.get('summary'))

                for group in groups:
                    if course in course_groups and group in course_groups[course]:
                        course_groups[course][group].append(c)
                    elif course in course_groups and group not in course_groups[course]:
                        course_groups[course][group] = [c]
                    else:
                        course_groups[course] = {group: [c]}
            else:
                everyone.append(c)

    return everyone, course_groups


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
    generate_ical_files(track_calendars)


if __name__ == "__main__":
    main()
