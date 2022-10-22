from dataclasses import dataclass
import timeslot

@dataclass
class SurveyData:
    """Class that holds the survey data for a student"""
    student_id: str
    timezone: str
    preffered_students: list[str]
    disliked_students: list[str]
    availability: list[timeslot.TimeSlot]

