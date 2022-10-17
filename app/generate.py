"""
generate contains the methods to generate a dataset of students
"""

from random import randint
from typing import List


class UserRecord:
    asurite = str
    preferred_students = List[str]
    disliked_students = List[str]
    days_available_by_time = dict

    def __init__(self) -> None:
        self.preferred_students = []
        self.disliked_students = []
        self.days_available_by_time = {}


def generate_random_dataset(count: int):
    """
    generates a random dataset to be used

    preferred students will be random for a set range
    disliked students will be random for a set range
    """
    asurites = []
    records = [UserRecord]

    for i in range(count):
        asurites.append(format(f'asurite{i}'))

    for i in asurites:
        user = UserRecord()
        user.asurite = i
        avail_students = asurites.copy()
        avail_students.remove(i)
        preferred_students = get_random_students(students=avail_students)
        disliked_students = get_random_students(students=avail_students)
        user.preferred_students = preferred_students
        user.disliked_students = disliked_students
        user.days_available_by_time = get_random_availability()
        records.append(user)
    for student in records:
        print(
            f'student: {student.asurite}, {student.preferred_students}, {student.disliked_students}, {student.days_available_by_time}'
        )

    return records


def get_random_students(students: List[str], max_count=5) -> List[str]:
    """
    generates a random selection of students with the max specified
    """

    rand_count = randint(0, max_count)
    rand_students = []
    for _ in range(rand_count):
        rand_student_idx = randint(0, len(students) - 1)
        rand_students.append(students[rand_student_idx])
        students.pop(rand_student_idx)

    return rand_students


def rand_days(num_days: int):
    days = [
        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
        'sunday'
    ]

    days_avail = [str]

    for _ in range(num_days):
        days_avail.append(days.pop(randint(0, len(days) - 1)))

    return days_avail


def get_random_availability(timeslice=3):
    """
    generates a dictionary with each timeslice of the day
    that contains a certain set of days the person is available
    """
    if 24 % timeslice != 0:
        raise Exception("cannot divide timeslice evenly")

    availability = {}
    interval_count = 24 // timeslice
    for i in range(interval_count):
        num_days_avail = randint(0, 6)
        availability[i] = rand_days(num_days_avail)

    return availability
