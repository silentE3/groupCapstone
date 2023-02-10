'''
Testing loader
'''
import copy
import datetime
import pytest
from app import models
from app import config
from app.data import load

# NOTE: These tests verify the functionality in read_dataset.py. Additionally,
#   in the process of doing so, they also verify the functionality in read_config.py.


# This test verifies that config_1.json and Example_Survey_Results_1.csv (both
# stored in the test_files folder) are read and processed correctly.
#
# Example_Survey_Results_1 consists of 4 records, three of are which are typical
#   records (some fields have values, others are blank) and a fourth where
#   the user has blank responses (did not fill out the survey).
#
# Additionally, each field in Example_Survey_Results_1 IS enclosed in double
#   quotes in order to verify that the program is capable of reading the file properly
#   in this situation.
#
def test_read_dataset_1():
    '''
    Read dataset 1 test
    '''
    # *************************************************************************
    # Start by building the expected user records
    # *************************************************************************

    # First user record -- jsmith1
    student_id_1 = 'jsmith1'
    timezone_1 = 'UTC +1'
    preferred_students_1 = ['jdoe2']
    disliked_students_1 = ['mmuster3', 'jschmo4']
    availability_1 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['Sunday', '', 'Friday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': ['Monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['']
    }
    user_record_1 = models.SurveyRecord(
        student_id=student_id_1,
        timezone=timezone_1,
        preferred_students=preferred_students_1,
        disliked_students=disliked_students_1,
        availability=availability_1
    )

    # Second user record -- jdoe2
    student_id_2 = 'jdoe2'
    timezone_2 = 'UTC +2'
    preferred_students_2 = ['mmuster3', 'jschmo4']
    disliked_students_2 = ['jsmith1', 'bwillia5']
    availability_2 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': ['Tuesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': ['Wednesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['']
    }
    user_record_2 = models.SurveyRecord(
        student_id=student_id_2,
        timezone=timezone_2,
        preferred_students=preferred_students_2,
        disliked_students=disliked_students_2,
        availability=availability_2
    )

    # Third user record -- mmuster3
    student_id_3 = 'mmuster3'
    timezone_3 = 'UTC +3'
    preferred_students_3 = ['jsmith1', 'bwillia5']
    disliked_students_3 = ['jdoe2']
    availability_3 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['Friday']
    }
    user_record_3 = models.SurveyRecord(
        student_id=student_id_3,
        timezone=timezone_3,
        preferred_students=preferred_students_3,
        disliked_students=disliked_students_3,
        availability=availability_3
    )

    # Fourth user record -- jschmo4 (NOTE: user did not fill out survey. i.e., has no responses)
    student_id_4 = 'jschmo4'
    timezone_4 = ''
    preferred_students_4 = []
    disliked_students_4 = []
    availability_4 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['']
    }
    user_record_4 = models.SurveyRecord(
        student_id=student_id_4,
        timezone=timezone_4,
        preferred_students=preferred_students_4,
        disliked_students=disliked_students_4,
        availability=availability_4
    )

    surveys_expected = [
        user_record_1,
        user_record_2,
        user_record_3,
        user_record_4
    ]

    # *************************************************************************
    # Read/process the config and survey data
    # *************************************************************************

    config_data: models.Configuration = config.read_json(
        "./tests/test_files/configs/config_1.json")

    surveys_result = load.read_survey(
        config_data['field_mappings'], './tests/test_files/survey_results/Example_Survey_Results_1.csv')

    # *************************************************************************
    # Verify that the config and survey data was read/processed properly.
    # *************************************************************************

    assert (len(surveys_result.records) == 4)  # 4 user records
    # assert (surveys_result == surveys_expected)

# This test verifies that config_1.json and Example_Survey_Results_2.csv (both
# stored in the test_files folder) are read and processed correctly.
#
# Example_Survey_Results_2 consists of 6 user records, all of are filled out
# "completely" (no blank fields).
#
# Additionally, each field in Example_Survey_Results_2 is NOT enclosed in double
#   quotes in order to verify that the program is capable of reading the file properly
#   in this situation.
#


def test_read_dataset_2():

    # *************************************************************************
    # Start by building the expected user records
    # *************************************************************************

    # First user record -- jsmith1
    student_id_1 = 'jsmith1'
    timezone_1 = 'UTC +1'
    preferred_students_1 = ['jdoe2', 'mmuster3',
                            'jschmo4', 'bwillia5', 'mbrown6']
    disliked_students_1 = ['jwhite7', 'ssilver8', 'hpotter9']
    availability_1 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['Sunday', 'Monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': ['Friday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': ['Monday', 'Tuesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': ['Monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': ['Wednesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': ['Monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['Friday']
    }
    user_record_1 = models.SurveyRecord(
        student_id=student_id_1,
        timezone=timezone_1,
        preferred_students=preferred_students_1,
        disliked_students=disliked_students_1,
        availability=availability_1
    )

    # Second user record -- jdoe2
    student_id_2 = 'jdoe2'
    timezone_2 = 'UTC +2'
    preferred_students_2 = ['mmuster3', 'jschmo4',
                            'bwillia5', 'mbrown6', 'jwhite7']
    disliked_students_2 = ['ssilver8', 'hpotter9', 'jsmith1']
    availability_2 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['Monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': ['Tuesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': ['Wednesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': ['Friday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': ['Saturday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': ['Sunday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['Monday']
    }
    user_record_2 = models.SurveyRecord(
        student_id=student_id_2,
        timezone=timezone_2,
        preferred_students=preferred_students_2,
        disliked_students=disliked_students_2,
        availability=availability_2
    )

    # Third user record -- mmuster3
    student_id_3 = 'mmuster3'
    timezone_3 = 'UTC +3'
    preferred_students_3 = ['jschmo4', 'bwillia5',
                            'mbrown6', 'jwhite7', 'ssilver8']
    disliked_students_3 = ['hpotter9', 'jsmith1', 'jdoe2']
    availability_3 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['Tuesday', 'Wednesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': ['Tuesday', 'Wednesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': ['Tuesday', 'Wednesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': ['Tuesday', 'Wednesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': ['Tuesday', 'Wednesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': ['Tuesday', 'Wednesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': ['Tuesday', 'Wednesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['Tuesday', 'Wednesday']
    }
    user_record_3 = models.SurveyRecord(
        student_id=student_id_3,
        timezone=timezone_3,
        preferred_students=preferred_students_3,
        disliked_students=disliked_students_3,
        availability=availability_3
    )

    # Fourth user record -- jschmo4
    student_id_4 = 'jschmo4'
    timezone_4 = 'UTC +2'
    preferred_students_4 = ['bwillia5', 'mbrown6',
                            'jwhite7', 'ssilver8', 'hpotter9']
    disliked_students_4 = ['jsmith1', 'jdoe2', 'mmuster3']
    availability_4 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['', 'Monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': ['Tuesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': ['', 'Monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': ['Tuesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': ['', 'Monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': ['Tuesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': ['', 'Monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['Tuesday']
    }
    user_record_4 = models.SurveyRecord(
        student_id=student_id_4,
        timezone=timezone_4,
        preferred_students=preferred_students_4,
        disliked_students=disliked_students_4,
        availability=availability_4
    )

    # User record 5 -- bwillia5
    student_id_5 = 'bwillia5'
    timezone_5 = 'UTC +5'
    preferred_students_5 = ['mbrown6', 'jwhite7',
                            'ssilver8', 'hpotter9', 'jsmith1']
    disliked_students_5 = ['jdoe2', 'mmuster3', 'jschmo4']
    availability_5 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['Monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': ['Tuesday', 'Wednesday', 'Saturday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': ['Friday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': ['Monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': ['Sunday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': ['Sunday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': ['Saturday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['Monday']
    }
    user_record_5 = models.SurveyRecord(
        student_id=student_id_5,
        timezone=timezone_5,
        preferred_students=preferred_students_5,
        disliked_students=disliked_students_5,
        availability=availability_5
    )

    # User record 6 -- mbrown6
    student_id_6 = 'mbrown6'
    timezone_6 = 'UTC +2'
    preferred_students_6 = ['jwhite7', 'ssilver8',
                            'hpotter9', 'jsmith1', 'jdoe2']
    disliked_students_6 = ['mmuster3', 'jschmo4', 'bwillia5']
    availability_6 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', '', 'Friday', 'Saturday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': ['Saturday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': ['Friday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': [''],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': ['Wednesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': ['Tuesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': ['Monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['Sunday']
    }
    user_record_6 = models.SurveyRecord(
        student_id=student_id_6,
        timezone=timezone_6,
        preferred_students=preferred_students_6,
        disliked_students=disliked_students_6,
        availability=availability_6
    )

    surveys_expected = [
        user_record_1,
        user_record_2,
        user_record_3,
        user_record_4,
        user_record_5,
        user_record_6
    ]

    # *************************************************************************
    # Read/process the config and survey data
    # *************************************************************************

    config_data = config.read_json("./tests/test_files/configs/config_1.json")
    surveys_result = load.read_survey(
        config_data['field_mappings'], './tests/test_files/survey_results/Example_Survey_Results_2.csv')

    # *************************************************************************
    # Verify that the config and survey data was read/processed properly.
    # *************************************************************************

    assert (len(surveys_result.records) == 6)  # 6 user records
    # assert (surveys_result == surveys_expected)

# This test verifies that config_1.json and Example_Survey_Results_3.csv (both
# stored in the test_files folder) are read and processed correctly.
#
# Example_Survey_Results_3 is testing a bit of a corner case where there are
# no user records.


def test_read_dataset_3():

    surveys_expected = []  # none

    # *************************************************************************
    # Read/process the config and survey data
    # *************************************************************************

    config_data = config.read_json("./tests/test_files/configs/config_1.json")
    surveys_result = load.read_survey(
        config_data['field_mappings'], './tests/test_files/survey_results/Example_Survey_Results_3.csv')

    # *************************************************************************
    # Verify that the config and survey data was read/processed properly.
    # *************************************************************************

    assert (len(surveys_result.records) == 0)  # 0 (no) user records
    assert (surveys_result.records == surveys_expected)

# This test verifies that config_2.json and Example_Survey_Results_4.csv (both
# stored in the test_files folder) are read and processed correctly.
#
# Note here that we are changing the config file to verify that this "configurability"
#  works as expected.
#
# Example_Survey_Results_4 details:
#   - Consists of 2 user records
#   - Each field is NOT enclosed in double quotes
#   - Begins with a BOM (Byte Order Mark)
#


def test_read_dataset_4():

    # *************************************************************************
    # Start by building the expected user records
    # *************************************************************************

    # First user record -- A1
    student_id_1 = 'A1'
    timezone_1 = 'UTC -5'
    preferred_students_1 = ['A27', 'A3', 'A16', 'A32', 'A20']
    disliked_students_1 = ['A12', 'A12', 'A12']
    availability_1 = {
        'Sunday - 0:00 AM - 3:00 AM': ['1'],
        'Sunday - 3:00 AM - 6:00 AM': ['1'],
        'Sunday - 6:00 AM - 9:00 AM': ['1'],
        'Sunday - 9:00 AM - 12:00 PM': ['1'],
        'Sunday - 12:00 PM - 3:00 PM': ['1'],
        'Sunday - 3:00 PM - 6:00 PM': ['1'],
        'Sunday - 6:00 PM - 9:00 PM': ['1'],
        'Sunday - 9:00 PM - 12:00 PM': ['1'],
        'Monday - 0:00 AM - 3:00 AM': [''],
        'Monday - 3:00 AM - 6:00 AM': [''],
        'Monday - 6:00 AM - 9:00 AM': [''],
        'Monday - 9:00 AM - 12:00 PM': [''],
        'Monday - 12:00 PM - 3:00 PM': [''],
        'Monday - 3:00 PM - 6:00 PM': ['1'],
        'Monday - 6:00 PM - 9:00 PM': ['1'],
        'Monday - 9:00 PM - 12:00 PM': ['1'],
        'Tuesday - 0:00 AM - 3:00 AM': [''],
        'Tuesday - 3:00 AM - 6:00 AM': [''],
        'Tuesday - 6:00 AM - 9:00 AM': [''],
        'Tuesday - 9:00 AM - 12:00 PM': [''],
        'Tuesday - 12:00 PM - 3:00 PM': [''],
        'Tuesday - 3:00 PM - 6:00 PM': [''],
        'Tuesday - 6:00 PM - 9:00 PM': ['1'],
        'Tuesday - 9:00 PM - 12:00 PM': ['1'],
        'Wednesday - 0:00 AM - 3:00 AM': [''],
        'Wednesday - 3:00 AM - 6:00 AM': [''],
        'Wednesday - 6:00 AM - 9:00 AM': [''],
        'Wednesday - 9:00 AM - 12:00 PM': [''],
        'Wednesday - 12:00 PM - 3:00 PM': [''],
        'Wednesday - 3:00 PM - 6:00 PM': ['1'],
        'Wednesday - 6:00 PM - 9:00 PM': ['1'],
        'Wednesday - 9:00 PM - 12:00 PM': ['1'],
        ' - 0:00 AM - 3:00 AM': [''],
        ' - 3:00 AM - 6:00 AM': [''],
        ' - 6:00 AM - 9:00 AM': [''],
        ' - 9:00 AM - 12:00 PM': [''],
        ' - 12:00 PM - 3:00 PM': [''],
        ' - 3:00 PM - 6:00 PM': [''],
        ' - 6:00 PM - 9:00 PM': ['1'],
        'Thursday - 9:00 PM - 12:00 PM': ['1'],
        'Friday - 0:00 AM - 3:00 AM': [''],
        'Friday - 3:00 AM - 6:00 AM': [''],
        'Friday - 6:00 AM - 9:00 AM': [''],
        'Friday - 9:00 AM - 12:00 PM': [''],
        'Friday - 12:00 PM - 3:00 PM': [''],
        'Friday - 3:00 PM - 6:00 PM': ['1'],
        'Friday - 6:00 PM - 9:00 PM': ['1'],
        'Friday - 9:00 PM - 12:00 PM': ['1'],
        'Saturday - 0:00 AM - 3:00 AM': ['1'],
        'Saturday - 3:00 AM - 6:00 AM': ['1'],
        'Saturday - 6:00 AM - 9:00 AM': ['1'],
        'Saturday - 9:00 AM - 12:00 PM': ['1'],
        'Saturday - 12:00 PM - 3:00 PM': ['1'],
        'Saturday - 3:00 PM - 6:00 PM': ['1'],
        'Saturday - 6:00 PM - 9:00 PM': ['1'],
        'Saturday - 9:00 PM - 12:00 PM': ['1']
    }
    user_record_1 = models.SurveyRecord(
        student_id=student_id_1,
        timezone=timezone_1,
        preferred_students=preferred_students_1,
        disliked_students=disliked_students_1,
        availability=availability_1
    )

    # Second user record -- A2
    student_id_2 = 'A2'
    timezone_2 = 'UTC -7'
    preferred_students_2 = ['A16', 'A1', 'A27', 'A32', 'A20']
    disliked_students_2 = ['A37']
    availability_2 = {
        'Sunday - 0:00 AM - 3:00 AM': [''],
        'Sunday - 3:00 AM - 6:00 AM': [''],
        'Sunday - 6:00 AM - 9:00 AM': ['1'],
        'Sunday - 9:00 AM - 12:00 PM': ['1'],
        'Sunday - 12:00 PM - 3:00 PM': ['1'],
        'Sunday - 3:00 PM - 6:00 PM': ['1'],
        'Sunday - 6:00 PM - 9:00 PM': ['1'],
        'Sunday - 9:00 PM - 12:00 PM': ['1'],
        'Monday - 0:00 AM - 3:00 AM': [''],
        'Monday - 3:00 AM - 6:00 AM': [''],
        'Monday - 6:00 AM - 9:00 AM': [''],
        'Monday - 9:00 AM - 12:00 PM': [''],
        'Monday - 12:00 PM - 3:00 PM': [''],
        'Monday - 3:00 PM - 6:00 PM': [''],
        'Monday - 6:00 PM - 9:00 PM': ['1'],
        'Monday - 9:00 PM - 12:00 PM': ['1'],
        'Tuesday - 0:00 AM - 3:00 AM': [''],
        'Tuesday - 3:00 AM - 6:00 AM': [''],
        'Tuesday - 6:00 AM - 9:00 AM': [''],
        'Tuesday - 9:00 AM - 12:00 PM': [''],
        'Tuesday - 12:00 PM - 3:00 PM': [''],
        'Tuesday - 3:00 PM - 6:00 PM': [''],
        'Tuesday - 6:00 PM - 9:00 PM': ['1'],
        'Tuesday - 9:00 PM - 12:00 PM': ['1'],
        'Wednesday - 0:00 AM - 3:00 AM': [''],
        'Wednesday - 3:00 AM - 6:00 AM': [''],
        'Wednesday - 6:00 AM - 9:00 AM': [''],
        'Wednesday - 9:00 AM - 12:00 PM': [''],
        'Wednesday - 12:00 PM - 3:00 PM': [''],
        'Wednesday - 3:00 PM - 6:00 PM': [''],
        'Wednesday - 6:00 PM - 9:00 PM': ['1'],
        'Wednesday - 9:00 PM - 12:00 PM': ['1'],
        'Thursday - 0:00 AM - 3:00 AM': [''],
        'Thursday - 3:00 AM - 6:00 AM': [''],
        'Thursday - 6:00 AM - 9:00 AM': [''],
        'Thursday - 9:00 AM - 12:00 PM': [''],
        'Thursday - 12:00 PM - 3:00 PM': [''],
        'Thursday - 3:00 PM - 6:00 PM': [''],
        'Thursday - 6:00 PM - 9:00 PM': ['1'],
        'Thursday - 9:00 PM - 12:00 PM': ['1'],
        'Friday - 0:00 AM - 3:00 AM': [''],
        'Friday - 3:00 AM - 6:00 AM': [''],
        'Friday - 6:00 AM - 9:00 AM': [''],
        'Friday - 9:00 AM - 12:00 PM': ['1'],
        'Friday - 12:00 PM - 3:00 PM': ['1'],
        'Friday - 3:00 PM - 6:00 PM': ['1'],
        'Friday - 6:00 PM - 9:00 PM': ['1'],
        'Friday - 9:00 PM - 12:00 PM': ['1'],
        'Saturday - 0:00 AM - 3:00 AM': [''],
        'Saturday - 3:00 AM - 6:00 AM': [''],
        'Saturday - 6:00 AM - 9:00 AM': ['1'],
        'Saturday - 9:00 AM - 12:00 PM': ['1'],
        'Saturday - 12:00 PM - 3:00 PM': ['1'],
        'Saturday - 3:00 PM - 6:00 PM': ['1'],
        'Saturday - 6:00 PM - 9:00 PM': ['1'],
        'Saturday - 9:00 PM - 12:00 PM': ['1']
    }
    user_record_2 = models.SurveyRecord(
        student_id=student_id_2,
        timezone=timezone_2,
        preferred_students=preferred_students_2,
        disliked_students=disliked_students_2,
        availability=availability_2
    )

    surveys_expected = [
        user_record_1,
        user_record_2
    ]

    # *************************************************************************
    # Read/process the config and survey data
    # *************************************************************************

    config_data = config.read_json("./tests/test_files/configs/config_2.json")

    surveys_result = load.read_survey(
        config_data['field_mappings'], './tests/test_files/survey_results/Example_Survey_Results_4.csv')

    # *************************************************************************
    # Verify that the config and survey data was read/processed properly.
    # *************************************************************************

    assert (len(surveys_result.records) == 2)  # 2 user records
    # assert (surveys_result == surveys_expected)

# This test verifies that config_1.json and Example_Survey_Results_1.csv (both
# stored in the test_files folder) are read and processed correctly.
#
# Example_Survey_Results_1 consists of 4 records, three of are which are typical
#   records (some fields have values, others are blank) and a fourth where
#   the user has blank responses (did not fill out the survey).
#
# Additionally, each field in Example_Survey_Results_1 IS enclosed in double
#   quotes in order to verify that the program is capable of reading the file properly
#   in this situation.
#


def test_read_dataset_1_all_fields():
    '''
    Just lie Read dataset 1 test but with all user fields
    '''
    config_data: models.Configuration = config.read_json(
        "./tests/test_files/configs/config_1_full.json")
    # *************************************************************************
    # Start by building the expected user records
    # *************************************************************************
    timestamp = datetime.datetime(2022, 10, 17, 18, 31, 58)
    # First user record -- jsmith1
    student_id_1 = 'jsmith1'
    student_email_1 = "jsmith1@asu.edu"
    student_name_1 = "John Smith"
    student_login_1 = "jsmith_1"
    timezone_1 = 'UTC +1'
    preferred_students_1 = ['jdoe2']
    disliked_students_1 = ['jschmo4', 'mmuster3']
    availability_1 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['sunday', 'thursday', 'friday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': ['monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': []
    }
    user_record_1 = models.SurveyRecord(
        student_id=student_id_1,
        timezone=timezone_1,
        student_email=student_email_1,
        student_name=student_name_1,
        student_login=student_login_1,
        preferred_students=preferred_students_1,
        disliked_students=disliked_students_1,
        availability=availability_1,
        submission_date=timestamp,
        has_matching_availability=False,
        provided_availability=True
    )

    # Second user record -- jdoe2
    student_id_2 = 'jdoe2'
    timezone_2 = 'UTC +2'
    student_email_2 = "jdoe2@asu.edu"
    student_name_2 = "Jane Doe"
    student_login_2 = "jdoe_2"
    preferred_students_2 = ['mmuster3', 'jschmo4']
    disliked_students_2 = ['jsmith1', 'bwillia5']
    availability_2 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': ['tuesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': ['wednesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': []
    }
    user_record_2 = models.SurveyRecord(
        student_id=student_id_2,
        timezone=timezone_2,
        student_email=student_email_2,
        student_name=student_name_2,
        student_login=student_login_2,
        preferred_students=preferred_students_2,
        disliked_students=disliked_students_2,
        availability=availability_2,
        submission_date=timestamp,
        has_matching_availability=False,
        provided_availability=True
    )

    # Third user record -- mmuster3
    student_id_3 = 'mmuster3'
    timezone_3 = 'UTC +3'
    student_email_3 = "mmuster3@asu.edu"
    student_name_3 = "Max Munster"
    student_login_3 = "mmuster_3"
    preferred_students_3 = ['jsmith1', 'bwillia5']
    disliked_students_3 = ['jdoe2']
    availability_3 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': ['thursday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['friday']
    }
    user_record_3 = models.SurveyRecord(
        student_id=student_id_3,
        timezone=timezone_3,
        student_email=student_email_3,
        student_name=student_name_3,
        student_login=student_login_3,
        preferred_students=preferred_students_3,
        disliked_students=disliked_students_3,
        availability=availability_3,
        submission_date=timestamp,
        has_matching_availability=False,
        provided_availability=True
    )

    surveys_expected = [
        user_record_1,
        user_record_2,
        user_record_3
    ]

    # *************************************************************************
    # Read/process the config and survey data
    # *************************************************************************

    surveys_result = load.read_survey(config_data['field_mappings'],
                                      './tests/test_files/survey_results/Example_Survey_Results_1_full.csv')

    # *************************************************************************
    # Verify that the config and survey data was read/processed properly.
    # *************************************************************************

    assert (len(surveys_result.records) == 3)
    assert surveys_result.records[0].availability == surveys_expected[0].availability
    assert surveys_result.records[1].preferred_students[0] in surveys_expected[1].preferred_students


def test_read_dataset_dup_user():
    '''
    tests loading a dataset that contains a duplicate user. It checks  that the latest submission is used
    '''
    config_data: models.Configuration = config.read_json(
        "./tests/test_files/configs/config_1_full.json")
    # *************************************************************************
    # Start by building the expected user records
    # *************************************************************************
    timestamp = datetime.datetime(2022, 10, 17, 18, 31, 58)
    # First user record -- jsmith1
    student_id_1 = 'jsmith1'
    student_email_1 = "jsmith1@asu.edu"
    student_name_1 = "John Smith"
    student_login_1 = "jsmith_1"
    timezone_1 = 'UTC +1'
    preferred_students_1 = ['jdoe2']
    disliked_students_1 = ['jschmo4', 'mmuster3']
    availability_1 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['sunday', 'thursday', 'friday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': ['monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': []
    }
    user_record_1 = models.SurveyRecord(
        student_id=student_id_1,
        timezone=timezone_1,
        student_email=student_email_1,
        student_name=student_name_1,
        student_login=student_login_1,
        preferred_students=preferred_students_1,
        disliked_students=disliked_students_1,
        availability=availability_1,
        submission_date=timestamp,
        has_matching_availability=False,
        provided_availability=True
    )

    # Second user record -- jdoe2
    student_id_2 = 'jdoe2'
    timezone_2 = 'UTC +2'
    student_email_2 = "jdoe2@asu.edu"
    student_name_2 = "Jane Doe"
    student_login_2 = "jdoe_2"
    preferred_students_2 = ['mmuster3', 'jschmo4']
    disliked_students_2 = ['jsmith1', 'bwillia5']
    availability_2 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['monday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': ['tuesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': ['wednesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': []
    }
    user_record_2 = models.SurveyRecord(
        student_id=student_id_2,
        timezone=timezone_2,
        student_email=student_email_2,
        student_name=student_name_2,
        student_login=student_login_2,
        preferred_students=preferred_students_2,
        disliked_students=disliked_students_2,
        availability=availability_2,
        submission_date=timestamp,
        has_matching_availability=False,
        provided_availability=True
    )

    # Third user record -- mmuster3. Has the latest record
    student_id_3 = 'mmuster3'
    timezone_3 = 'UTC +3'
    student_email_3 = "mmuster3@asu.edu"
    student_name_3 = "Max Munster"
    student_login_3 = "mmuster_3"
    preferred_students_3 = ['jsmith1', 'bwillia5']
    disliked_students_3 = ['jdoe2']
    availability_3 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['monday', 'tuesday'],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': [],
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['friday']
    }
    user_record_3 = models.SurveyRecord(
        student_id=student_id_3,
        timezone=timezone_3,
        student_email=student_email_3,
        student_name=student_name_3,
        student_login=student_login_3,
        preferred_students=preferred_students_3,
        disliked_students=disliked_students_3,
        availability=availability_3,
        submission_date=timestamp,
        has_matching_availability=False,
        provided_availability=True
    )

    surveys_expected = [
        user_record_1,
        user_record_2,
        user_record_3
    ]

    # *************************************************************************
    # Read/process the config and survey data
    # *************************************************************************

    surveys_result = load.read_survey(config_data['field_mappings'],
                                      './tests/test_files/survey_results/Example_Survey_Results_7_dup_user.csv')

    # *************************************************************************
    # Verify that the config and survey data was read/processed properly.
    # *************************************************************************

    assert (len(surveys_result.records) == 3)
    # cheks that the latest is used if it is greater
    assert surveys_result.records[0].availability == surveys_expected[0].availability
    # checks that the latest is used if it is equal in timestamp
    assert surveys_result.records[2].availability == surveys_expected[2].availability
    # checks that it doesn't match to a dup record with older timestamp
    assert not surveys_result.records[1].availability == surveys_expected[1].availability


def test_total_availability_matches_finds_matches():
    student = models.SurveyRecord(student_id='asurite1', availability={
        '1': ['monday', 'tuesday'],
        '2': ['monday', 'tuesday']
    })

    student_list = [
        models.SurveyRecord('asurite2', availability={
            '1': ['monday'],
            '2': ['tuesday']
        }),
        models.SurveyRecord('asurite2', availability={
            '1': ['monday'],
            '2': ['tuesday']
        }),
        models.SurveyRecord('asurite2', availability={
            '1': ['tuesday'],
            '2': ['tuesday']
        })
    ]

    matches = load.total_availability_matches(student, student_list)
    assert matches == 6


def test_total_availability_matches_empty_string():
    student = models.SurveyRecord(student_id='asurite1', availability={
        '1': ['monday', ''],
    })

    student_list = [
        models.SurveyRecord('asurite2', availability={
            '1': [],
        }),
        models.SurveyRecord('asurite2', availability={
            '1': ['monday'],
        }),
        models.SurveyRecord('asurite2', availability={
            '1': ['tuesday'],
        })
    ]

    matches = load.total_availability_matches(student, student_list)

    assert matches == 1


def test_wildcard_availability_sets_all_avail():
    avail_fields = ['1', '2', '3']

    avail = load.wildcard_availability(avail_fields)

    assert avail['1'] == ['monday', 'tuesday', 'wednesday',
                          'thursday', 'friday', 'saturday', 'sunday']
    assert avail['2'] == ['monday', 'tuesday', 'wednesday',
                          'thursday', 'friday', 'saturday', 'sunday']
    assert avail['3'] == ['monday', 'tuesday', 'wednesday',
                          'thursday', 'friday', 'saturday', 'sunday']


def test_preprocess_survey_data_good_avail():
    students = [
        models.SurveyRecord('asurite1', availability={
            '1': ['monday'],
        }, provided_availability=True),
        models.SurveyRecord('asurite2', availability={
            '1': ['monday'],
        }, provided_availability=True),
        models.SurveyRecord('asurite3', availability={
            '1': ['monday'],
        }, provided_availability=True)
    ]

    students_copy = copy.deepcopy(students)
    config: models.SurveyFieldMapping = {
        'student_id_field_name': 'asurite',
        'student_name_field_name': 'name',
        'student_email_field_name': '',
        'student_login_field_name': '',
        'timezone_field_name': '',
        'submission_timestamp_field_name': '',
        'preferred_students_field_names': [],
        'disliked_students_field_names': [],
        'availability_field_names': ['1', '2', '3']
    }

    load.preprocess_survey_data(students, config)

    assert students == students_copy


def test_preprocess_survey_data_bad_avail():
    students = [
        models.SurveyRecord('asurite1', availability={
                            '1': []}, provided_availability=False),
        models.SurveyRecord('asurite2', availability={
                            '1': []}, provided_availability=False),
        models.SurveyRecord('asurite3', availability={
                            '1': ['sunday']}, provided_availability=True)
    ]

    students_copy = copy.deepcopy(students)
    config: models.SurveyFieldMapping = {
        'student_id_field_name': 'asurite',
        'student_name_field_name': 'name',
        'student_email_field_name': '',
        'student_login_field_name': '',
        'timezone_field_name': '',
        'submission_timestamp_field_name': '',
        'preferred_students_field_names': [],
        'disliked_students_field_names': [],
        'availability_field_names': ['1']
    }

    load.preprocess_survey_data(students, config)

    assert not students == students_copy
    assert students[0].availability['1'] == ['monday', 'tuesday',
                                             'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    assert students[2].availability['1'] == ['sunday']
    assert not students[1].availability == []


def test_parse_survey_record_fails_on_student_id():
    config: models.SurveyFieldMapping = {
        'student_id_field_name': 'asurite',
        'student_name_field_name': 'name',
        'student_email_field_name': 'email',
        'student_login_field_name': 'github user',
        'timezone_field_name': 'timezone',
        'submission_timestamp_field_name': 'submission_date',
        'preferred_students_field_names': ['pref 1', 'pref 2'],
        'disliked_students_field_names': ['disl 1', 'disl 2'],
        'availability_field_names': ['1']
    }

    row: dict = {
        'asurite': '',
        'name': 'billy',
        'email': 'billy@hotmail.com',
        'github user': 'billy123',
        'timezone': 'UTC-3',
        'submission_date': '2022/10/22 6:30:11 PM MDT',
        'disl 1': 'asurite2',
        'disl 2': '',
        'pref 1': 'asurite3',
        'pref 2': '',
        '1': 'monday;tuesday'
    }
    with pytest.raises(AttributeError):
        record = load.parse_survey_record(config, row)


def test_parse_survey_record_maps_single_field():
    config: models.SurveyFieldMapping = {
        'student_id_field_name': 'asurite',
        'student_name_field_name': 'name',
        'student_email_field_name': 'email',
        'student_login_field_name': 'github user',
        'timezone_field_name': 'timezone',
        'submission_timestamp_field_name': 'submission_date',
        'preferred_students_field_names': ['pref 1', 'pref 2'],
        'disliked_students_field_names': ['disl 1', 'disl 2'],
        'availability_field_names': ['1']
    }

    row: dict = {
        'asurite': 'asurite1',
        'name': 'billy',
        'email': 'billy@hotmail.com',
        'github user': 'billy123',
        'timezone': 'UTC-3',
        'submission_date': '2022/10/22 6:30:11 PM MDT',
        'disl 1': 'asurite2',
        'disl 2': '',
        'pref 1': 'asurite3',
        'pref 2': '',
        '1': 'monday;tuesday'
    }

    record = load.parse_survey_record(config, row)

    assert len(record.availability['1']) == 2
    assert not len(record.disliked_students) == 2
    assert 'asurite3' in record.preferred_students
    assert len(record.student_id) > 0


def test_parse_survey_record_with_white_space():
    config: models.SurveyFieldMapping = {
        'student_id_field_name': 'asurite',
        'student_name_field_name': 'name',
        'student_email_field_name': 'email',
        'student_login_field_name': 'github user',
        'timezone_field_name': 'timezone',
        'submission_timestamp_field_name': 'submission_date',
        'preferred_students_field_names': ['pref 1', 'pref 2'],
        'disliked_students_field_names': ['disl 1'],
        'availability_field_names': ['1', '2', '3', '4', '5']
    }

    row: dict = {
        'asurite': 'asurite1 ',
        'name': 'billy ',
        'email': 'billy@hotmail.com ',
        'github user': 'billy123 ',
        'timezone': 'UTC-3 ',
        'submission_date': '2022/10/22 6:30:11 PM MDT',
        'disl 1': 'asurite2 ',
        'pref 1': ' asurite3',
        'pref 2': ' ',
        '1': 'monday ;tuesday',
        '2': 'wednesday\t;thursday',
        '3': 'friday\n;saturday',
        '4': 'monday; tuesday',
        '5': ' '
    }

    record = load.parse_survey_record(config, row)

    assert record.availability['1'][0] == 'monday'
    assert record.availability['2'][0] == 'wednesday'
    assert record.availability['3'][0] == 'friday'
    assert record.availability['4'][1] == 'tuesday'
    assert len(record.availability['5']) == 0
    assert record.timezone == 'UTC-3'
    assert record.student_email == 'billy@hotmail.com'
    assert record.student_name == 'billy'
    assert record.student_login == 'billy123'
    assert record.student_id == 'asurite1'
    assert record.preferred_students[0] == 'asurite3'
    assert len(record.preferred_students) == 1
    assert record.disliked_students[0] == 'asurite2'


def test_read_survey():
    print('hi')


def test_parse_asurite():

    asurites = ['asurite 123124 -123123',
                'asurite', 'asurite  1234', '  asurite ']

    for asurite in asurites:
        assert load.parse_asurite(asurite) == 'asurite'
        a = load.parse_asurite(asurite)


def test_load_group_data():
    '''
    Tests the loading of grouping data
    '''
    config_data: models.Configuration = config.read_json(
        "./tests/test_files/dev_data/config-dev.json")
    survey_data = load.read_survey(
        config_data['field_mappings'], "./tests/test_files/dev_data/dataset-dev.csv")
    groups = load.read_groups(
        "./tests/test_files/dev_data/output.csv", survey_data.records)

    assert len(groups) == 4
    assert len(groups[0].members) == 5
    assert len(groups[1].members) == 5
    assert len(groups[2].members) == 5
    assert len(groups[3].members) == 5


def test_load_missing_students_1():
    '''
    Tests the add missing student function with 2 missing students.
    '''
    result = []

    ids = []
    ids.append("asurite1")
    ids.append("asurite2")
    ids.append("asurite3")
    ids.append("asurite4")
    ids.append("asurite5")
    ids.append("asurite6")

    survey = []
    student1 = models.SurveyRecord("asurite1")
    student2 = models.SurveyRecord("asurite2")
    student3 = models.SurveyRecord("asurite3")
    student4 = models.SurveyRecord("asurite4")
    survey.append(student1)
    survey.append(student2)
    survey.append(student3)
    survey.append(student4)

    fields = [
        "0 to 3 AM",
        "3 to 6 AM",
        "6 to 9 AM",
        "9 to 12 PM",
        "12 to 3 PM",
        "3 to 6 PM",
        "6 to 9 PM",
        "9 to 12 AM"
    ]

    result = load.add_missing_students(survey, ids, fields)

    assert len(result) == 6
    assert result[4].availability == {
        "0 to 3 AM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        "3 to 6 AM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        "6 to 9 AM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        "9 to 12 PM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        "12 to 3 PM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        "3 to 6 PM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        "6 to 9 PM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        "9 to 12 AM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    }
    assert result[5].availability == {
        "0 to 3 AM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        "3 to 6 AM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        "6 to 9 AM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        "9 to 12 PM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        "12 to 3 PM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        "3 to 6 PM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        "6 to 9 PM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        "9 to 12 AM": ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    }
    assert result[4].provided_survey_data == False
    assert result[5].provided_survey_data == False


def test_load_missing_students_2():
    '''
    Tests the add missing student function with 0 missing students.
    '''
    result = []

    ids = []
    ids.append("asurite1")
    ids.append("asurite2")
    ids.append("asurite3")
    ids.append("asurite4")

    survey = []
    student1 = models.SurveyRecord("asurite1")
    student2 = models.SurveyRecord("asurite2")
    student3 = models.SurveyRecord("asurite3")
    student4 = models.SurveyRecord("asurite4")
    survey.append(student1)
    survey.append(student2)
    survey.append(student3)
    survey.append(student4)

    fields = [
        "0 to 3 AM",
        "3 to 6 AM",
        "6 to 9 AM",
        "9 to 12 PM",
        "12 to 3 PM",
        "3 to 6 PM",
        "6 to 9 PM",
        "9 to 12 AM"
    ]

    result = load.add_missing_students(survey, ids, fields)

    assert len(result) == 4
    assert result[0].provided_survey_data == True
    assert result[1].provided_survey_data == True
    assert result[2].provided_survey_data == True
    assert result[3].provided_survey_data == True


def test_load_missing_students_3():
    '''
    Tests the add missing student function with 0 missing students.
    '''
    result = []

    ids = []
    ids.append("asurite1")
    ids.append("asurite2")
    ids.append("asurite3")
    ids.append("asurite4")

    survey = []

    fields = [
        "0 to 3 AM",
        "3 to 6 AM",
        "6 to 9 AM",
        "9 to 12 PM",
        "12 to 3 PM",
        "3 to 6 PM",
        "6 to 9 PM",
        "9 to 12 AM"
    ]

    result = load.add_missing_students(survey, ids, fields)

    assert len(result) == 4
    assert result[0].provided_survey_data == False
    assert result[1].provided_survey_data == False
    assert result[2].provided_survey_data == False
    assert result[3].provided_survey_data == False


def test_read_roster():
    '''
    Tests to see if program reads the roster file correctly
    '''
    students = []
    students = load.read_roster("roster.csv")

    assert len(students) == 20
    students[0] = "asurite1"
    students[1] = "asurite2"
    students[2] = "asurite3"
    students[3] = "asurite4"
    students[4] = "asurite5"
    students[5] = "asurite6"
    students[6] = "asurite7"
    students[7] = "asurite8"
    students[8] = "asurite9"
    students[9] = "asurite10"
    students[10] = "asurite11"
    students[11] = "asurite12"
    students[12] = "asurite13"
    students[13] = "asurite14"
    students[14] = "asurite15"
    students[15] = "asurite16"
    students[16] = "asurite17"
    students[17] = "asurite18"
    students[18] = "asurite19"
    students[19] = "asurite20"

# This test verifies that Example_Report_1.xlsx is read and processed correctly via
#  the read_report function. In the process, it also verifies the __parse_record and
#  __parse_availability functions.
#
# Example_Report_1.xlsx consists of 5 students, three of which are typical
#   records (some fields have values, others are blank) and a two where
#   the user has blank responses (did not fill out the survey).
#
# NOTE: Currently, we are only concerned with properly reading in the student's:
#       - asurite (student_id)
#       - disliked students
#       - preferred students
#       - availability
#       - assigned group (group_id)
#   If this were to change in the future, then this test should be updated as necessary.

def test_read_report():
    '''
    Read report 1 test
    '''
    # *************************************************************************
    # Start by building the expected user records
    # *************************************************************************

    # First user record -- jsmith1
    student_id_1 = 'jsmith1'
    timezone_1 = 'UTC +1'
    preferred_students_1 = ['jdoe2']
    disliked_students_1 = ['mmuster3', 'jschmo4']
    availability_1 = {
        '0:00 AM - 3:00 AM': ['sunday', 'thursday', 'friday'],
        '3:00 AM - 6:00 AM': ['monday', 'tuesday'],
        '6:00 AM - 9:00 AM': [],
        '9:00 AM - 12:00 PM': [],
        '12:00 PM - 3:00 PM': [],
        '3:00 PM - 6:00 PM': ['tuesday', 'wednesday'],
        '6:00 PM - 9:00 PM': [],
        '9:00 PM - 12:00 PM': []
    }
    user_record_1 = models.SurveyRecord(
        student_id=student_id_1,
        preferred_students=preferred_students_1,
        disliked_students=disliked_students_1,
        availability=availability_1,
        group_id='1'
    )

    # Second user record -- jdoe2
    student_id_2 = 'jdoe2'
    timezone_2 = 'UTC +2'
    preferred_students_2 = ['mmuster3', 'jschmo4']
    disliked_students_2 = ['jsmith1', 'bwillia5']
    availability_2 = {
        '0:00 AM - 3:00 AM': [],
        '3:00 AM - 6:00 AM': ['monday', 'tuesday'],
        '6:00 AM - 9:00 AM': [],
        '9:00 AM - 12:00 PM': [],
        '12:00 PM - 3:00 PM': ['tuesday'],
        '3:00 PM - 6:00 PM': ['wednesday'],
        '6:00 PM - 9:00 PM': [],
        '9:00 PM - 12:00 PM': []
    }
    user_record_2 = models.SurveyRecord(
        student_id=student_id_2,
        preferred_students=preferred_students_2,
        disliked_students=disliked_students_2,
        availability=availability_2,
        group_id='2'
    )

    # Third user record -- mmuster3
    student_id_3 = 'mmuster3'
    timezone_3 = 'UTC +3'
    preferred_students_3 = ['jsmith1', 'bwillia5']
    disliked_students_3 = ['jdoe2']
    availability_3 = {
        '0:00 AM - 3:00 AM': [],
        '3:00 AM - 6:00 AM': ['monday', 'tuesday'],
        '6:00 AM - 9:00 AM': [],
        '9:00 AM - 12:00 PM': [],
        '12:00 PM - 3:00 PM': [],
        '3:00 PM - 6:00 PM': ['wednesday', 'thursday'],
        '6:00 PM - 9:00 PM': ['thursday'],
        '9:00 PM - 12:00 PM': ['friday']
    }
    user_record_3 = models.SurveyRecord(
        student_id=student_id_3,
        preferred_students=preferred_students_3,
        disliked_students=disliked_students_3,
        availability=availability_3,
        group_id='1'
    )

    # Fourth user record -- jschmo4 (NOTE: user did not fill out survey. i.e., has no responses and therefore gets
    # assigned completely open availability)
    student_id_4 = 'jschmo4'
    timezone_4 = ''
    preferred_students_4 = []
    disliked_students_4 = []
    availability_4 = {
        '0:00 AM - 3:00 AM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        '3:00 AM - 6:00 AM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        '6:00 AM - 9:00 AM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        '9:00 AM - 12:00 PM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        '12:00 PM - 3:00 PM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        '3:00 PM - 6:00 PM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        '6:00 PM - 9:00 PM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        '9:00 PM - 12:00 PM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    }
    user_record_4 = models.SurveyRecord(
        student_id=student_id_4,
        preferred_students=preferred_students_4,
        disliked_students=disliked_students_4,
        availability=availability_4,
        group_id='2'
    )

    # Fifth user record -- jbwillia5 (NOTE: user did not fill out survey. i.e., has no responses and therefore gets
    # assigned completely open availability)
    student_id_5 = 'bwillia5'
    timezone_5 = ''
    preferred_students_5 = []
    disliked_students_5 = []
    availability_5 = {
        '0:00 AM - 3:00 AM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        '3:00 AM - 6:00 AM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        '6:00 AM - 9:00 AM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        '9:00 AM - 12:00 PM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        '12:00 PM - 3:00 PM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        '3:00 PM - 6:00 PM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        '6:00 PM - 9:00 PM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        '9:00 PM - 12:00 PM': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    }
    user_record_5 = models.SurveyRecord(
        student_id=student_id_5,
        preferred_students=preferred_students_5,
        disliked_students=disliked_students_5,
        availability=availability_5,
        group_id='1'
    )

    expected_students: models.GroupRecord = models.GroupRecord(
        "expected students",
        [
            user_record_1,
            user_record_2,
            user_record_3,
            user_record_4,
            user_record_5
        ]
    )

    # *************************************************************************
    # Read/process the config and survey data
    # *************************************************************************

    report_data = load.read_report(
        './tests/test_files/reports/Example_Report_1.xlsx')

    # *************************************************************************
    # Verify that the config and survey data was read/processed properly.
    # *************************************************************************
    assert len(report_data[0]) == 2  # 2 group records
    num_students: int = 0
    for group in report_data[0]:
        for student in group.members:
            # Each student record is read in as expected
            assert __student_in_group(student, expected_students)
            num_students += 1
    assert num_students == 5  # 5 student records


def __survey_record_eq(record1: models.SurveyRecord, record2: models.SurveyRecord) -> bool:
    # Helper function to determine if record1 and record2 are equivalent.
    if not record1.student_id == record2.student_id:
        return False
    if not record1.student_name == record2.student_name:
        return False
    if not record1.student_email == record2.student_email:
        return False
    if not record1.student_login == record2.student_login:
        return False
    if not record1.timezone == record2.timezone:
        return False
    if not record1.preferred_students == record2.preferred_students:
        for preferred_student in record1.preferred_students:
            if not preferred_student in record2.preferred_students:
                return False
        for preferred_student in record2.preferred_students:
            if not preferred_student in record1.preferred_students:
                return False
    if not record1.disliked_students == record2.disliked_students:
        for disliked_student in record1.disliked_students:
            if not disliked_student in record2.disliked_students:
                return False
        for disliked_student in record2.disliked_students:
            if not disliked_student in record1.disliked_students:
                return False
    if not record1.availability == record2.availability:
        return False
    if not record1.group_id == record2.group_id:
        return False
    return True


def __student_in_group(student: models.SurveyRecord, group: models.GroupRecord) -> bool:
    # Helper function to determine if an equivalent survey record for 'student' exists
    # in 'group'
    student_in_group: bool = False
    for group_student in group.members:
        if __survey_record_eq(student, group_student):
            student_in_group = True
    return student_in_group

def test_split_on_delimiter():
    '''
    Tests to see if the program splits on delimiter correctly. This was found
    as a limitation of the current implementation and that this test will be
    revisited when split_on_delimiters is changed.
    '''
    availability = "Monday|Tuesday|Wednesday|Thursday|Friday"
    delimiter = "|"

    list = load.split_on_delimiters(availability, delimiter)

    print(list)
    days = []
    day = ""
    for i in range(len(list)):
        if (list[i] != "|"):
            day += list[i]
            if (i == len(list)-1):
                days.append(day)
        else:
            days.append(day)
            day = ""
    
    print(days)
    assert days[0] == "Monday"
    assert days[1] == "Tuesday"
    assert days[2] == "Wednesday"
    assert days[3] == "Thursday"
    assert days[4] == "Friday"

def test_split_on_delimiter_2():
    '''
    Tests to see if the program splits on multiple delimiters correctly.
    '''
    availability = "Monday;Tuesday;Wednesday:Thursday:Friday"
    delimiter = ";:"

    list = load.split_on_delimiters(availability, delimiter)

    print(list)

    assert list[0] == "Monday"
    assert list[1] == "Tuesday"
    assert list[2] == "Wednesday"
    assert list[3] == "Thursday"
    assert list[4] == "Friday"

def test_split_on_delimiter_3():
    '''
    Tests to see if the program splits on delimiter correctly with a different delimiter other than |.
    '''
    availability = "Monday;Tuesday;Wednesday;Thursday;Friday"
    delimiter = ";"

    list = load.split_on_delimiters(availability, delimiter)

    print(list)
    assert list[0] == "Monday"
    assert list[1] == "Tuesday"
    assert list[2] == "Wednesday"
    assert list[3] == "Thursday"
    assert list[4] == "Friday"
