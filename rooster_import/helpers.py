from .models import Course, Calendar


def parse_request(request_body):
    """
    Validate whether the given request body contains dictionaries that
    represent a course and (some of) its associated groups.
    """
    courses = []
    groups = []

    # Check if data type is list and its length is greater than 0.
    if not isinstance(request_body, list) or len(request_body) < 1:
        return {"icalUrl": "Error: Invalid request"}

    for course_dict in request_body:
        # Check if data type is dict and the expected keys are present.
        if (
            not isinstance(course_dict, dict)
            or "id" not in course_dict
            or "group" not in course_dict
        ):
            return {"icalUrl": "Error: Invalid request"}

        try:
            course = Course.objects.get(id=course_dict["id"])
            courses.append(course)
        except Course.DoesNotExist:
            return {"icalUrl": "Error: course {} does not exist".format(course_dict["id"])}

        if course_dict["group"] == "":
            groups += [group for group in course.group_set.all()]
        else:
            group_set = course.group_set.filter(id=course_dict["group"])

            if not group_set.exists():
                return {"icalUrl": "Error: Group {} does not exist for course {}".format(course_dict["group"], course.id)}

            groups.append(group_set.first())

    calendar = Calendar.objects

    for course in courses:
        calendar = calendar.filter(courses=course)

    for group in groups:
        calendar = calendar.filter(groups=group)

    if calendar.exists():
        calendar = calendar.first()
    else:
        calendar = Calendar()
        calendar.save()
        [calendar.courses.add(course) for course in courses]
        [calendar.groups.add(group) for group in groups]
        calendar.generate()

    return {"icalUrl": calendar.get_url()}
