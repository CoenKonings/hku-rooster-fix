from .models import Course, Calendar, CourseLecturerSelection, Lecturer


def parse_request(request_body):
    """
    Validate whether the given request body contains dictionaries that
    represent a course and (some of) its associated groups.
    """
    courses_lecturers = []
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
            or "lecturers" not in course_dict
        ):
            return {"icalUrl": "Error: Invalid request"}

        try:
            course = Course.objects.get(id=course_dict["id"])
        except Course.DoesNotExist:
            return {
                "icalUrl": "Error: course {} does not exist".format(course_dict["id"])
            }

        if course_dict["group"] == "":
            groups += [group for group in course.group_set.all()]
        else:
            group_set = course.group_set.filter(id=course_dict["group"])

            if not group_set.exists():
                return {
                    "icalUrl": "Error: Group {} does not exist for course {}".format(
                        course_dict["group"], course.id
                    )
                }

            groups.append(group_set.first())

        if len(course_dict["lecturers"]) > 0 and course_dict["lecturers"] != [""]:
            lecturers = []

            for lecturer_id in course_dict["lecturers"]:
                if lecturer_id == "":
                    continue

                try:
                    lecturer = Lecturer.objects.filter(id=lecturer_id).first()
                    lecturers.append(lecturer)
                except Lecturer.DoesNotExist:
                    return {
                        "icalUrl": "Error: Lecturer {} does not exist.".format(
                            lecturer_id
                        )
                    }

            c_l_s = CourseLecturerSelection(course=course)
            c_l_s.save()
            [c_l_s.lecturers.add(lecturer) for lecturer in lecturers]
            courses_lecturers.append(c_l_s)
        else:
            c_l_s = CourseLecturerSelection(course=course)
            c_l_s.save()
            courses_lecturers.append(c_l_s)


    calendar = Calendar()
    calendar.save()

    for course_lecturers in courses_lecturers:
        course_lecturers.calendar = calendar
        course_lecturers.save()

    [calendar.groups.add(group) for group in groups]
    calendar.generate()

    return {"icalUrl": calendar.get_url()}
