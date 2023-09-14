from .models import Course, Group


def validate_request(request_body):
    """
    Validate whether the given request body contains dictionaries that
    represent a course and (some of) its associated groups.
    """

    # Check if data type is list and its length is greater than 0.
    if not isinstance(request_body, list) or len(request_body) < 1:
        return False

    for course_dict in request_body:
        # Check if data type is dict and the expected keys are present.
        if (
            not isinstance(course_dict, dict)
            or "id" not in course_dict
            or "group" not in course_dict
        ):
            return False

        # Check if a course with the given ID exists.
        if not Course.objects.get(id=course_dict["id"]):
            return False

        # Check if each group ID corresponds to an entry in the database.
        for group_id in course_dict["group"]:
            if not Group.objects.get(id=group_id):
                return False

    return True
