"""This will read in the survey data from the dataset CSV file and parse it based on the 
grouping config. The first line of the dataset data is assumed to be header data."""

from io import TextIOWrapper
from app.data_classes import config, survey_data

def load_survey_data_csv(dataset_path: str, config_data: config.GroupingConfig) -> list[survey_data.SurveyData]:
    """Loads the survey data form the CSV file into a list of survey data classes.
    Uses the header from the CSV file to get each field value based on the config data."""
    dataset_file = open(dataset_path, mode="r", encoding="UTF-8")
    header_indexes = load_header(dataset_file)
    surveys = list()

    while data := dataset_file.readline():
 
        student_id = ""
        timezone = ""
        preffered_students = list()
        disliked_students = list()
        availability = dict()
        data_fields = data.split(",")

 
        # The nested [] looks confusing but we are just getting the index for the
        # # name of the field and then the value at that index in the data_fields

        # student id
        if config_data["student_id_field_name"] in header_indexes:
            student_id = data_fields[header_indexes[config_data["student_id_field_name"]]]

        # time zone
        if config_data["timezone_field_name"] in header_indexes:
            timezone = data_fields[header_indexes[config_data["timezone_field_name"]]]

        #preferred students
        for ps in config_data["preferred_students_field_names"]:
            if ps in header_indexes:
                preffered_students.append(data_fields[header_indexes[ps]])


        #disliked students
        for ds in config_data["disliked_students_field_names"]:
            if ds in header_indexes:
                disliked_students.append(data_fields[header_indexes[ds]])

        #availability 
        for a in config_data["availability_field_names"]:
            if a in header_indexes:                 
                availability[a] = (not (data_fields[header_indexes[a]].strip().lower() == "false")
                    and not (data_fields[header_indexes[a]].strip() == "0") 
                    and not data_fields[header_indexes[a]])

        surveys.append(
            survey_data.SurveyData(
                student_id, 
                timezone,
                preffered_students, 
                disliked_students, 
                availability))

    return surveys


def load_header(dataset_file: TextIOWrapper) -> dict[str, int]:
    """Loads the headers from the CSV into a dictionary where each field name
    has a corresponding index number, starting from 0. This will allow us to
    get the index number for a field based on the header name and retrieve
    the value from an ordered list."""
    header_text = dataset_file.readline()
    header_text = header_text.replace("\ufeff", "")    # clear the endian marker
    headers = header_text.split(",")
    i = 0
    headers_dict = dict()
    for h in headers:
        headers_dict[h] = i
        i += 1    
    return headers_dict

