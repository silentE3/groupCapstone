'''config holds the logic to read in a configuration object'''
import json
from app.models import Configuration


def read_json(config_path: str) -> Configuration:
    """Reads in a json configuration file"""
    with open(config_path, mode="r", encoding="UTF-8") as json_file:
        data: Configuration = json.load(json_file)

#The following global module variables and assignments are a move towards
#creating a single instance of the configuration that does not need to be
#passed to each method.

    global class_name #: str
    global target_group_size #: int
    global grouping_passes #: int
    global availability_values_delimiter #: str
    global field_mappings #: SurveyFieldMapping
    global report_fields #: ReportConfiguration
    global output_student_name #: bool
    global output_student_email #: bool
    global output_student_login #: bool

    class_name = data["class_name"] if "class_name" in data.keys() else "Unknown"
    target_group_size = data["target_group_size"] if "target_group_size" in data.keys() else 5
    grouping_passes = data["grouping_passes"] if "grouping_passes" in data.keys() else 10
    availability_values_delimiter = data["availability_values_delimiter"] if "availability_values_delimiter" in data.keys() else ";"
    field_mappings = data["field_mappings"] if "field_mappings" in data.keys() else None
    report_fields = data["report_fields"] if "report_fields" in data.keys() else None
    output_student_name =  data["output_student_name"] if "output_student_name" in data.keys() else False
    output_student_email = data["output_student_email"] if "output_student_email" in data.keys() else False
    output_student_login = data["output_student_login"] if "output_student_login" in data.keys() else False

    return data


