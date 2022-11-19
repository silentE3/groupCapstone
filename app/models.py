
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
class ReportConfiguration(TypedDict):
    '''
    Data class for the report layout
    '''

    # show preferred students found in the grouping
    show_preferred_students: bool

    # show disliked students found in the grouping
    show_disliked_students: bool

    # show availability that matched in the grouping
    show_availability_overlap: bool

    # show group-level and solution-level scores
    show_scores: bool


@dataclass
class Configuration(TypedDict):
    """Data class for the app configuration"""
    class_name: str
    target_group_size: int
    grouping_passes: int
    field_mappings: SurveyFieldMapping
    report_fields: ReportConfiguration
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
    okay_with_rank = 0
    avail_rank = 0

    def __lt__(self, other):
        return self.okay_with_rank + self.avail_rank < other.okay_with_rank + other.avail_rank


@dataclass
class GroupRecord:
    '''
    Class that holds group infomation for a single group
    '''
    group_id: str = ""
    members: list[SurveyRecord] = field(default_factory=list)


@dataclass
class GroupSetData:
    '''
    Class that holds set information for a group set
    '''
    scoring_id: str  # e.g. "solution_x" if scoring a group set or group_id if scoring a group
    num_groups_no_overlap: int
    num_of_disliked_pairs: int
    num_of_preferred_pairs: int
    target_group_size: int
    num_of_preferred_slots: int
    num_of_students: int
