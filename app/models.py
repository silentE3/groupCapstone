
'''module that holds the model definitions in the application'''
from dataclasses import dataclass, field
from typing import TypedDict


@dataclass
class SurveyFieldMapping(TypedDict):
    '''
    Data class for the mapping of the raw data fields
    '''
    student_id_field_name: str
    student_name_field_name: str
    student_email_field_name: str
    student_login_field_name: str
    timezone_field_name: str
    preferred_students_field_names: list[str]
    disliked_students_field_names: list[str]
    availability_field_names: list[str]


@dataclass
class Configuration(TypedDict):
    """Data class for the app configuration"""
    class_name: str
    target_group_size: int
    grouping_passes: int
    field_mappings: SurveyFieldMapping
    output_student_name: bool
    output_student_email: bool
    output_student_login: bool


@dataclass
class SurveyRecord:
    """Data class that describes a single record in the survey dataset"""
    student_id: str
    student_name: str = ""
    student_email: str = ""
    student_login: str = ""
    timezone: str = field(default_factory=str)
    preferred_students: list[str] = field(default_factory=list)
    disliked_students: list[str] = field(default_factory=list)
    availability: dict[str, list[str]] = field(default_factory=dict)



@dataclass
class GroupRecord:
    '''
    Class that holds group infomation for a single group
    '''
    group_id: str
    members: list[SurveyRecord]