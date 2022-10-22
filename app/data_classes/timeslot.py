from dataclasses import dataclass

@dataclass
class TimeSlot:
    """Class for time slot availability"""
    time_of_day: str
    is_available: bool