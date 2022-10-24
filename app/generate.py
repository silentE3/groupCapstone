"""
generate contains the methods to generate a dataset for use in the application
"""

from dataclasses import dataclass, field
from random import randint


@dataclass
class UserRecord:
    """
    Describes a single record in the ingested dataset
    """
    asurite: str = field(default_factory=str)
    preferred_students: list[str] = field(default_factory=list)
    disliked_students: list[str] = field(default_factory=list)
    days_available_by_time: dict[int, list[str]] = field(default_factory=dict)


def format_records_as_table(records: list[UserRecord]) -> list[list[str]]:
    """
    takes in a list of user records
    and generates a 2d array(list) that can be used for output to a csv file.

    # Rows
    1: asurite
    2-10: availability - 8 fields for 3 hour increments during the day
    11-15: preferred students - 5 fields for up to 5 preferred students
    16-18: disliked students - 3 fields for up to 3 disliked students
    """
    body: list[list[str]] = []
    for record in records:
        row: list[str] = []
        row.append(record.asurite)
        for item in list(record.days_available_by_time.values()):
            row.append(','.join(item))
        for i in range(5):
            if i < len(record.preferred_students):
                row.append(record.preferred_students[i])
            else:
                row.append("")
        for i in range(3):
            if i < len(record.disliked_students):
                row.append(record.disliked_students[i])
            else:
                row.append("")
        body.append(row)
    return body


def generate_random_user_records(count: int) -> list[UserRecord]:
    """
    generates a random dataset to be used

    preferred students will be random for a set range
    disliked students will be random for a set range
    time availability is randomized
    """

    if count <= 1:
        raise Exception("count must be greater than 1")

    asurites = []
    records = []

    for i in range(count):
        asurites.append(format(f'asurite{i}'))

    for i in asurites:
        user = UserRecord(i)
        avail_students = asurites.copy()
        avail_students.remove(i)
        preferred_students = get_random_students(students=avail_students)
        disliked_students = get_random_students(students=avail_students)
        user.preferred_students = preferred_students
        user.disliked_students = disliked_students
        user.days_available_by_time = get_random_availability()
        records.append(user)
    return records


def get_random_students(students: list[str], max_count=5) -> list[str]:
    """
    generates a random selection of students with the max specified
    """

    max_count = max_count if max_count < len(students) else len(students)

    rand_count = randint(0, max_count)
    rand_students = []
    if rand_count == 0:
        return rand_students

    for _ in range(rand_count):
        rand_student_idx = randint(0, len(students) - 1)
        rand_students.append(students[rand_student_idx])
        students.pop(rand_student_idx)

    return rand_students


def rand_days(num_days: int) -> list[str]:
    """
    generates a random list of days
    """
    days = [
        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
        'sunday'
    ]

    days_avail: list[str] = []

    for _ in range(num_days):
        days_avail.append(days.pop(randint(0, len(days) - 1)))

    return days_avail


def get_random_availability(timeslice=3) -> dict:
    """
    generates a dictionary with each timeslice (hour) of the day
    that contains a certain set of days the person is available
    """
    if 24 % timeslice != 0:
        raise Exception("cannot divide timeslice evenly")

    availability = {}
    interval_count = 24 // timeslice
    for i in range(interval_count):
        num_days_avail = randint(0, 6)
        availability[str(i)] = rand_days(num_days_avail)

    return availability
