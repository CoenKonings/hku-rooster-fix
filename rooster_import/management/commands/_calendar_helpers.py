import requests
import os
from hku_rooster_fix.settings import BASE_DIR
from rooster_import.models import Track, Course, Group, Event
from icalendar import Calendar


def get_calendar_feed(calendar_name, url):
    """
    Download ICS file containing all events for all groups of all tracks.
    """
    r = requests.get(url)

    if not os.path.isdir(os.path.join(BASE_DIR, "rooster_import", "calendars")):
        os.mkdir(os.path.join(BASE_DIR, "rooster_import", "calendars"))

    open(
        os.path.join(BASE_DIR, "rooster_import", "calendars", calendar_name + ".ics"),
        "wb",
    ).write(r.content)


def groups_from_event_name(name):
    """
    Find the group numbers and course name from an event name.
    """
    groups = []
    course_name = ""

    if "groep" in name.lower() and "hele groep" not in name.lower():
        for word in name.split(" "):
            if word.lower() == "groep" or word.lower() == "en":
                continue
            elif word.isnumeric() or len(word) == 2 and word[0].isnumeric():
                groups.append(word)
            else:
                course_name += word + " "
    else:
        course_name = name

    return course_name.strip(), groups


def tracks_from_event(event):
    """
    Find the tracks for which this event is relevant.
    """
    tracks = Track.objects.all()
    relevant_tracks = []
    attendees = event.get("attendee")

    if attendees:
        for attendee in attendees:
            attendee_name = attendee.params["CN"]

            for track in tracks:
                if track.name == attendee_name:
                    relevant_tracks.append(track)

    else:
        for track in tracks:
            if track.name == "relevant for everyone":
                relevant_tracks.append(track)

    return relevant_tracks


def store_course(course_name, tracks):
    """
    Retrieve the course with the given name from the database. If it does not
    exist, create it and save it to the database.
    """
    try:
        course = Course.objects.get(name=course_name)
        for track in tracks:
            course.tracks.add(track)
    except Course.DoesNotExist:
        course = Course(name=course_name)
        course.save()

        for track in tracks:
            course.tracks.add(track)

    return course


def store_groups(course, group_names):
    """
    Retrieve the groups for the given course with the given names. If they do
    not exist, save them to the database.
    """
    groups = []

    for group_name in group_names:
        try:
            group = Group.objects.get(name=group_name, course=course)
        except Group.DoesNotExist:
            group = Group(name=group_name, course=course)
            group.save()

        course.group_set.add(group)
        groups.append(group)

    return groups


def store_event(event):
    """
    Store the event. If necessary, add the associated courses and groups.
    """
    summary = event.get("summary")
    location = event.get("location")
    start = event.decoded("dtstart")
    end = event.decoded("dtend")

    tracks = tracks_from_event(event)
    course_name, group_names = groups_from_event_name(summary)
    course = store_course(course_name, tracks)
    groups = store_groups(course, group_names)

    event = Event(
        description=summary, location=location, course=course, start=start, end=end
    )
    event.save()
    [event.groups.add(group) for group in groups]


def calendar_to_database(calendar_name):
    """
    Read the calendar from an ical file and save it to the database.
    """
    with open(
        os.path.join(BASE_DIR, "rooster_import", "calendars", calendar_name + ".ics"),
        "rb",
    ) as calendar_file:
        mt2_totaal = Calendar.from_ical(calendar_file.read())

    for component in mt2_totaal.walk():
        if component.name == "VEVENT":
            store_event(component)
