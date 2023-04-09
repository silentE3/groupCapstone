
'''module that holds the model definitions in the application'''
from dataclasses import dataclass, field
import datetime as dt
from typing import TypedDict, Optional, ClassVar


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
    submission_timestamp_field_name: str
    preferred_students_field_names: list[str]
    disliked_students_field_names: list[str]
    availability_field_names: list[str]


@dataclass
class ReportConfiguration(TypedDict):
    '''
    Data class for the report layout
    TODO: Add additional attributes to this
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
    target_plus_one_allowed: bool
    target_minus_one_allowed: bool
    no_survey_group_method: int
    grouping_passes: int
    availability_values_delimiter: str
    field_mappings: SurveyFieldMapping
    report_fields: ReportConfiguration
    output_student_name: bool
    output_student_email: bool
    output_student_login: bool
    prioritize_preferred_over_availability: bool

@dataclass
class SurveyRecord:
    """Data class that describes a single record in the survey dataset"""
    student_id: str
    submission_date: dt.datetime = dt.datetime.now()
    student_name: str = ""
    student_email: str = ""
    student_login: str = ""
    timezone: str = field(default_factory=str)
    preferred_students: list[str] = field(default_factory=list)
    disliked_students: list[str] = field(default_factory=list)
    availability: dict[str, list[str]] = field(default_factory=dict)
    okay_with_rank = 0
    avail_rank = 0
    has_matching_availability: bool = True
    provided_availability: bool = True
    provided_survey_data: bool = True
    provided_pref_students: bool = True
    pref_pairing_possible: bool = True
    group_id: str = ""
    lock_in_group: bool = False

    def __lt__(self, other):
        return self.okay_with_rank + self.avail_rank < other.okay_with_rank + other.avail_rank


@dataclass
class SurveyData:
    """
    Data class for survey data loaded when reading in the raw survey file. 
    This holds both the raw csv rows from the file and the list of survey records 
    """
    records: list[SurveyRecord]
    raw_rows: list[list[str]]


@dataclass
class GroupRecord:
    '''
    Class that holds group infomation for a single group
    '''
    group_id: str
    members: list[SurveyRecord] = field(default_factory=list)


@dataclass
class GroupSetData:
    '''
    Class that holds set information for a group set
    '''
    scoring_id: str  # e.g. "solution_x" if scoring a group set or group_id if scoring a group
    target_group_size: int
    num_survey_preferred_slots: int
    num_students: int
    num_survey_time_slots: int
    # Default assignment of 0  for the items below b/c their iniital values are "don't
    # care" (reassigned as necessary) when being used to score INDIVIDUAL groups
    num_groups_no_overlap: int = 0
    num_disliked_pairs: int = 0
    num_preferred_pairs: int = 0
    num_additional_overlap: int = 0
    # NOTE: A student should only be included in the num_students_no_pref_pairs value below if they
    # don't have a preferred pair AND they theoretically could (they listed preferred student(s)
    # and at least one of these student(s) did not list them as disliked).
    num_students_no_pref_pairs: int = 0
    num_additional_pref_pairs: int = 0


@dataclass
class Scenario:
    '''
    scenario for a new group. includes the score, result group, and the removed user if they exist
    '''
    group: GroupRecord
    score: float
    removed_user: Optional[SurveyRecord] = field(default=None)

    def __lt__(self, other):
        return self.score < other.score


@dataclass
class SwapScenario:
    '''
    scenario for swapping a group
    '''
    group_1: GroupRecord
    group_2: GroupRecord
    score: float

    def __lt__(self, other):
        return self.score < other.score


@dataclass
class NoSurveyGroupMethodConsts:
    ''' 
    Data class for storing constants representing the valid methods that can be used
     to group students who didn't submit a survey.
    '''
    STANDARD_GROUPING: ClassVar[int] = 0
    DISTRIBUTE_EVENLY: ClassVar[int] = 1
    GROUP_TOGETHER: ClassVar[int] = 2


@dataclass
class GroupAvailabilityMap:
    '''
    data structure for a spread-out availability map
    per user per group
    users is a dictionary of users with the key being the user id
    and the value being a list of bools indicating availability for 
    a time slot
    '''
    group_id: str
    users: dict[str, list[bool]]


@dataclass
class AvailabilityMap:
    '''
    data structure that holds a list of the availability slots
    and the individual times for each slot

    '''

    availability_slots: dict[str, list[str]]
    group_availability: list[GroupAvailabilityMap]
