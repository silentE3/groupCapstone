
'''Class for the config information'''
from dataclasses import dataclass
from typing import TypedDict

@dataclass
class GroupingConfig(TypedDict):
    """Data class for configuration information"""
    class_name: str
    student_id_field_name: str
    timezone_field_name: str
    preferred_students_field_names: list[str]
    disliked_students_field_names: list[str]
    availability_field_names: list[str]
    min_group_size: int
    max_group_size: int
    grouping_passes: int
    