"""
module for the implementation of the grouping algorithm
"""
from app import models
from app.group import validate


class Algorithm:

    def __init__(self, students) -> None:
        self.students: list[models.SurveyRecord] = students
        self.groups: list[models.GroupRecord] = []

    def group_students(self) -> list[models.GroupRecord]:
        while len(self.students) > 0:
            student = self.students.pop()

            self.add_student_to_group(student)

        return self.groups

    def add_student_to_group(self, student: models.SurveyRecord):
        for group in self.groups:
            if not len(group.members) < 5:
                continue

            if len(validate.user_dislikes_group(student, group)) < 1 and validate.user_matches_availability_count(student, group) > 0:
                group.members.append(student)
                return

        if len(self.groups) < len(self.students) // 4:
            self.groups.append(models.GroupRecord())
            self.groups[-1].members.append(student)
            return
        else:
            for group in self.groups:
                if 

        print(student.student_id)


def total_dislike_incompatible_students(student: models.SurveyRecord, students: list[models.SurveyRecord]) -> int:
    """
    function to identify the total number of students that are disliked
    This should be the total count of incompatible students for the student.
    If the dislike is reciprical, don't count it twice.

    Args:
        student (models.SurveyRecord): student to check
        students (list[models.SurveyRecord]): full list of students

    Returns:
        int: number of total incompatible students
    """
    disliked_set: set[str] = set(student.disliked_students)

    for other_student in students:
        if student.student_id == other_student.student_id:
            continue

        if student.student_id in other_student.disliked_students:
            disliked_set.add(other_student.student_id)

    return len(disliked_set)


def total_availability_matches(student: models.SurveyRecord, students: list[models.SurveyRecord]) -> int:
    """
    checks the student's availability against everyone elses and counts the number of times that they match

    Args:
        student (models.SurveyRecord): student to check matches for
        students (list[models.SurveyRecord]): full list of students

    Returns:
        int: number of times the student matches availability in the dataset
    """

    totals = 0

    for other_student in students:
        if student.student_id == other_student.student_id:
            continue

        for time, avail_days in other_student.availability.items():
            for avail_day in avail_days:
                if avail_day in student.availability[time] and not avail_day == '':
                    totals += 1

    return totals


def rank_students(students: list[models.SurveyRecord]):
    for student in students:
        student.avail_rank = total_availability_matches(student, students)
        student.okay_with_rank = len(
            students) - total_dislike_incompatible_students(student, students)

    students.sort(reverse=True)


def pick_group():
    """
    how do I choose what group to join?

    generate a ranking of the available groups
    generate a ranking with a scenario for how it would change the overall score

    start at score of 100
    subtract for dislikes
    add for any matching availabilities
    how would adding a new user to the group work?
    how would swapping a user with the group work?
    how would a new group work
    how would the group limits work? Should it be a threshold? If it would result in a very good group score, it can break the boundary
    """

def run_scenario(user):
    """
    We need the ability to run a scenario when adding a user to a group. If
    """