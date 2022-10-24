from app.data_classes import survey_data
from app.file import read_config
from app.file.read_dataset import SurveyDataReader

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

    # *************************************************************************
    # Start by building the expected user records
    # *************************************************************************

    #First user record -- jsmith1
    student_id_1 = 'jsmith1'
    timezone_1 = 'UTC +1'
    preferred_students_1 = ['jdoe2 - Jane Doe']
    disliked_students_1 = ['mmuster3 - Max Mustermann', 'jschmo4 - Joe Schmo']
    availability_1 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['Sunday', 'Thursday', 'Friday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': ['Monday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': [''], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': [''], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': [''], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': [''], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': [''], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['']
        }
    user_record_1 = survey_data.SurveyData(
        student_id_1, 
        timezone_1, 
        preferred_students_1, 
        disliked_students_1, 
        availability_1
        )
    
    #Second user record -- jdoe2
    student_id_2 = 'jdoe2'
    timezone_2 = 'UTC +2'
    preferred_students_2 = ['mmuster3 - Max Mustermann', 'jschmo4 - Joe Schmo']
    disliked_students_2 = ['jsmith1 - John Smith', 'bwillia5 - Billy Williams']
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
    user_record_2 = survey_data.SurveyData(
        student_id_2, 
        timezone_2, 
        preferred_students_2,
        disliked_students_2, 
        availability_2
        )

    #Third user record -- mmuster3
    student_id_3 = 'mmuster3'
    timezone_3 = 'UTC +3'
    preferred_students_3 = ['jsmith1 - John Smith', 'bwillia5 - Billy Williams']
    disliked_students_3 = ['jdoe2 - Jane Doe']
    availability_3 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': [''], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': [''], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': [''], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': [''], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': [''], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': [''], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': ['Thursday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['Friday']
    }
    user_record_3 = survey_data.SurveyData(
        student_id_3, 
        timezone_3, 
        preferred_students_3,
        disliked_students_3, 
        availability_3
        )

    #Fourth user record -- jschmo4 (NOTE: user did not fill out survey. i.e., has no responses)
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
    user_record_4 = survey_data.SurveyData(
        student_id_4, 
        timezone_4, 
        preferred_students_4,
        disliked_students_4, 
        availability_4
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
    
    config_data = read_config.read_config_json("./tests/test_files/configs/config_1.json")
    survey_reader = SurveyDataReader(config_data)
    
    surveys_result = survey_reader.load('./tests/test_files/survey_results/Example_Survey_Results_1.csv')
    

    # *************************************************************************
    # Verify that the config and survey data was read/processed properly.
    # *************************************************************************

    assert(len(surveys_result) == 4) #4 user records
    assert(surveys_result == surveys_expected)

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

    #First user record -- jsmith1
    student_id_1 = 'jsmith1'
    timezone_1 = 'UTC +1'
    preferred_students_1 = ['jdoe2 - Jane Doe', 'mmuster3 - Max Mustermann', 'jschmo4 - Joe Schmo', 'bwillia5 - Billy Williams', 'mbrown6 - Mary Brown']
    disliked_students_1 = ['jwhite7 - Jack White', 'ssilver8 - Sarah Silver', 'hpotter9 - Harry Potter']
    availability_1 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['Sunday', 'Monday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': ['Thursday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': ['Friday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': ['Monday', 'Tuesday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': ['Monday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': ['Wednesday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': ['Monday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['Friday']
        }
    user_record_1 = survey_data.SurveyData(
        student_id_1, 
        timezone_1, 
        preferred_students_1, 
        disliked_students_1, 
        availability_1
        )
    
    #Second user record -- jdoe2
    student_id_2 = 'jdoe2'
    timezone_2 = 'UTC +2'
    preferred_students_2 = ['mmuster3 - Max Mustermann', 'jschmo4 - Joe Schmo', 'bwillia5 - Billy Williams', 'mbrown6 - Mary Brown', 'jwhite7 - Jack White']
    disliked_students_2 = ['ssilver8 - Sarah Silver', 'hpotter9 - Harry Potter', 'jsmith1 - John Smith']
    availability_2 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['Monday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': ['Tuesday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': ['Wednesday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': ['Thursday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': ['Friday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': ['Saturday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': ['Sunday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['Monday']
        }
    user_record_2 = survey_data.SurveyData(
        student_id_2, 
        timezone_2, 
        preferred_students_2,
        disliked_students_2, 
        availability_2
        )

    #Third user record -- mmuster3
    student_id_3 = 'mmuster3'
    timezone_3 = 'UTC +3'
    preferred_students_3 = ['jschmo4 - Joe Schmo', 'bwillia5 - Billy Williams', 'mbrown6 - Mary Brown', 'jwhite7 - Jack White', 'ssilver8 - Sarah Silver']
    disliked_students_3 = ['hpotter9 - Harry Potter', 'jsmith1 - John Smith', 'jdoe2 - Jane Doe']
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
    user_record_3 = survey_data.SurveyData(
        student_id_3, 
        timezone_3, 
        preferred_students_3,
        disliked_students_3, 
        availability_3
        )

    #Fourth user record -- jschmo4
    student_id_4 = 'jschmo4'
    timezone_4 = 'UTC +2'
    preferred_students_4 = ['bwillia5 - Billy Williams', 'mbrown6 - Mary Brown', 'jwhite7 - Jack White', 'ssilver8 - Sarah Silver', 'hpotter9 - Harry Potter']
    disliked_students_4 = ['jsmith1 - John Smith', 'jdoe2 - Jane Doe', 'mmuster3 - Max Mustermann']
    availability_4 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['Thursday', 'Monday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': ['Tuesday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': ['Thursday', 'Monday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': ['Tuesday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': ['Thursday', 'Monday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': ['Tuesday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': ['Thursday', 'Monday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['Tuesday']
    }
    user_record_4 = survey_data.SurveyData(
        student_id_4, 
        timezone_4, 
        preferred_students_4,
        disliked_students_4, 
        availability_4
        )


    # User record 5 -- bwillia5
    student_id_5 = 'bwillia5'
    timezone_5 = 'UTC +5'
    preferred_students_5 = ['mbrown6 - Mary Brown', 'jwhite7 - Jack White', 'ssilver8 - Sarah Silver', 'hpotter9 - Harry Potter', 'jsmith1 - John Smith']
    disliked_students_5 = ['jdoe2 - Jane Doe', 'mmuster3 - Max Mustermann', 'jschmo4 - Joe Schmo']
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
    user_record_5 = survey_data.SurveyData(
        student_id_5, 
        timezone_5, 
        preferred_students_5,
        disliked_students_5, 
        availability_5
        )

    # User record 6 -- mbrown6
    student_id_6 = 'mbrown6'
    timezone_6 = 'UTC +2'
    preferred_students_6 = ['jwhite7 - Jack White', 'ssilver8 - Sarah Silver', 'hpotter9 - Harry Potter', 'jsmith1 - John Smith', 'jdoe2 - Jane Doe']
    disliked_students_6 = ['mmuster3 - Max Mustermann', 'jschmo4 - Joe Schmo', 'bwillia5 - Billy Williams']
    availability_6 = {
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]': ['Saturday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]': ['Friday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]': ['Thursday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]': ['Wednesday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]': ['Tuesday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]': ['Monday'], 
        'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]': ['Sunday']
    }
    user_record_6 = survey_data.SurveyData(
        student_id_6, 
        timezone_6, 
        preferred_students_6,
        disliked_students_6, 
        availability_6
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
    
    config_data = read_config.read_config_json("./tests/test_files/configs/config_1.json")
    survey_reader = SurveyDataReader(config_data)
    
    surveys_result = survey_reader.load('./tests/test_files/survey_results/Example_Survey_Results_2.csv')

    # *************************************************************************
    # Verify that the config and survey data was read/processed properly.
    # *************************************************************************

    assert(len(surveys_result) == 6) #6 user records
    assert(surveys_result == surveys_expected)

# This test verifies that config_1.json and Example_Survey_Results_3.csv (both
# stored in the test_files folder) are read and processed correctly.
#
# Example_Survey_Results_3 is testing a bit of a corner case where there are
# no user records.
def test_read_dataset_3():

    surveys_expected = [] #none

    # *************************************************************************
    # Read/process the config and survey data
    # *************************************************************************
    
    config_data = read_config.read_config_json("./tests/test_files/configs/config_1.json")
    survey_reader = SurveyDataReader(config_data)
    
    surveys_result = survey_reader.load('./tests/test_files/survey_results/Example_Survey_Results_3.csv')
    

    # *************************************************************************
    # Verify that the config and survey data was read/processed properly.
    # *************************************************************************

    assert(len(surveys_result) == 0) # 0 (no) user records
    assert(surveys_result == surveys_expected)

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

    #First user record -- A1
    student_id_1 = 'A1'
    timezone_1 = 'UTC -5'
    preferred_students_1 = ['A27', 'A3', 'A16', 'A32', 'A20']
    disliked_students_1 = ['A12','A12','A12']
    availability_1 = {
        'Sunday - 0:00 AM - 3:00 AM' : ['1'],
        'Sunday - 3:00 AM - 6:00 AM' : ['1'],
        'Sunday - 6:00 AM - 9:00 AM' : ['1'],
        'Sunday - 9:00 AM - 12:00 PM' : ['1'],
        'Sunday - 12:00 PM - 3:00 PM' : ['1'],
        'Sunday - 3:00 PM - 6:00 PM' : ['1'],
        'Sunday - 6:00 PM - 9:00 PM' : ['1'],
        'Sunday - 9:00 PM - 12:00 PM' : ['1'],
        'Monday - 0:00 AM - 3:00 AM' : [''],
        'Monday - 3:00 AM - 6:00 AM' : [''],
        'Monday - 6:00 AM - 9:00 AM' : [''],
        'Monday - 9:00 AM - 12:00 PM' : [''],
        'Monday - 12:00 PM - 3:00 PM' : [''],
        'Monday - 3:00 PM - 6:00 PM' : ['1'],
        'Monday - 6:00 PM - 9:00 PM' : ['1'],
        'Monday - 9:00 PM - 12:00 PM' : ['1'],
        'Tuesday - 0:00 AM - 3:00 AM' : [''],
        'Tuesday - 3:00 AM - 6:00 AM' : [''],
        'Tuesday - 6:00 AM - 9:00 AM' : [''],
        'Tuesday - 9:00 AM - 12:00 PM' : [''],
        'Tuesday - 12:00 PM - 3:00 PM' : [''],
        'Tuesday - 3:00 PM - 6:00 PM' : [''],
        'Tuesday - 6:00 PM - 9:00 PM' : ['1'],
        'Tuesday - 9:00 PM - 12:00 PM' : ['1'],
        'Wednesday - 0:00 AM - 3:00 AM' : [''],
        'Wednesday - 3:00 AM - 6:00 AM' : [''],
        'Wednesday - 6:00 AM - 9:00 AM' : [''],
        'Wednesday - 9:00 AM - 12:00 PM' : [''],
        'Wednesday - 12:00 PM - 3:00 PM' : [''],
        'Wednesday - 3:00 PM - 6:00 PM' : ['1'],
        'Wednesday - 6:00 PM - 9:00 PM' : ['1'],
        'Wednesday - 9:00 PM - 12:00 PM' : ['1'],
        'Thursday - 0:00 AM - 3:00 AM' : [''],
        'Thursday - 3:00 AM - 6:00 AM' : [''],
        'Thursday - 6:00 AM - 9:00 AM' : [''],
        'Thursday - 9:00 AM - 12:00 PM' : [''],
        'Thursday - 12:00 PM - 3:00 PM' : [''],
        'Thursday - 3:00 PM - 6:00 PM' : [''],
        'Thursday - 6:00 PM - 9:00 PM' : ['1'],
        'Thursday - 9:00 PM - 12:00 PM' : ['1'],
        'Friday - 0:00 AM - 3:00 AM' : [''],
        'Friday - 3:00 AM - 6:00 AM' : [''],
        'Friday - 6:00 AM - 9:00 AM' : [''],
        'Friday - 9:00 AM - 12:00 PM' : [''],
        'Friday - 12:00 PM - 3:00 PM' : [''],
        'Friday - 3:00 PM - 6:00 PM' : ['1'],
        'Friday - 6:00 PM - 9:00 PM' : ['1'],
        'Friday - 9:00 PM - 12:00 PM' : ['1'],
        'Saturday - 0:00 AM - 3:00 AM' : ['1'],
        'Saturday - 3:00 AM - 6:00 AM' : ['1'],
        'Saturday - 6:00 AM - 9:00 AM' : ['1'],
        'Saturday - 9:00 AM - 12:00 PM' : ['1'],
        'Saturday - 12:00 PM - 3:00 PM' : ['1'],
        'Saturday - 3:00 PM - 6:00 PM' : ['1'],
        'Saturday - 6:00 PM - 9:00 PM' : ['1'],
        'Saturday - 9:00 PM - 12:00 PM' : ['1']
    }
    user_record_1 = survey_data.SurveyData(
        student_id_1, 
        timezone_1, 
        preferred_students_1, 
        disliked_students_1, 
        availability_1
        )
    
    #Second user record -- A2
    student_id_2 = 'A2'
    timezone_2 = 'UTC -7'
    preferred_students_2 = ['A16', 'A1', 'A27', 'A32', 'A20']
    disliked_students_2 = ['A37']
    availability_2 = {
        'Sunday - 0:00 AM - 3:00 AM' : [''],
        'Sunday - 3:00 AM - 6:00 AM' : [''],
        'Sunday - 6:00 AM - 9:00 AM' : ['1'],
        'Sunday - 9:00 AM - 12:00 PM' : ['1'],
        'Sunday - 12:00 PM - 3:00 PM' : ['1'],
        'Sunday - 3:00 PM - 6:00 PM' : ['1'],
        'Sunday - 6:00 PM - 9:00 PM' : ['1'],
        'Sunday - 9:00 PM - 12:00 PM' : ['1'],
        'Monday - 0:00 AM - 3:00 AM' : [''],
        'Monday - 3:00 AM - 6:00 AM' : [''],
        'Monday - 6:00 AM - 9:00 AM' : [''],
        'Monday - 9:00 AM - 12:00 PM' : [''],
        'Monday - 12:00 PM - 3:00 PM' : [''],
        'Monday - 3:00 PM - 6:00 PM' : [''],
        'Monday - 6:00 PM - 9:00 PM' : ['1'],
        'Monday - 9:00 PM - 12:00 PM' : ['1'],
        'Tuesday - 0:00 AM - 3:00 AM' : [''],
        'Tuesday - 3:00 AM - 6:00 AM' : [''],
        'Tuesday - 6:00 AM - 9:00 AM' : [''],
        'Tuesday - 9:00 AM - 12:00 PM' : [''],
        'Tuesday - 12:00 PM - 3:00 PM' : [''],
        'Tuesday - 3:00 PM - 6:00 PM' : [''],
        'Tuesday - 6:00 PM - 9:00 PM' : ['1'],
        'Tuesday - 9:00 PM - 12:00 PM' : ['1'],
        'Wednesday - 0:00 AM - 3:00 AM' : [''],
        'Wednesday - 3:00 AM - 6:00 AM' : [''],
        'Wednesday - 6:00 AM - 9:00 AM' : [''],
        'Wednesday - 9:00 AM - 12:00 PM' : [''],
        'Wednesday - 12:00 PM - 3:00 PM' : [''],
        'Wednesday - 3:00 PM - 6:00 PM' : [''],
        'Wednesday - 6:00 PM - 9:00 PM' : ['1'],
        'Wednesday - 9:00 PM - 12:00 PM' : ['1'],
        'Thursday - 0:00 AM - 3:00 AM' : [''],
        'Thursday - 3:00 AM - 6:00 AM' : [''],
        'Thursday - 6:00 AM - 9:00 AM' : [''],
        'Thursday - 9:00 AM - 12:00 PM' : [''],
        'Thursday - 12:00 PM - 3:00 PM' : [''],
        'Thursday - 3:00 PM - 6:00 PM' : [''],
        'Thursday - 6:00 PM - 9:00 PM' : ['1'],
        'Thursday - 9:00 PM - 12:00 PM' : ['1'],
        'Friday - 0:00 AM - 3:00 AM' : [''],
        'Friday - 3:00 AM - 6:00 AM' : [''],
        'Friday - 6:00 AM - 9:00 AM' : [''],
        'Friday - 9:00 AM - 12:00 PM' : ['1'],
        'Friday - 12:00 PM - 3:00 PM' : ['1'],
        'Friday - 3:00 PM - 6:00 PM' : ['1'],
        'Friday - 6:00 PM - 9:00 PM' : ['1'],
        'Friday - 9:00 PM - 12:00 PM' : ['1'],
        'Saturday - 0:00 AM - 3:00 AM' : [''],
        'Saturday - 3:00 AM - 6:00 AM' : [''],
        'Saturday - 6:00 AM - 9:00 AM' : ['1'],
        'Saturday - 9:00 AM - 12:00 PM' : ['1'],
        'Saturday - 12:00 PM - 3:00 PM' : ['1'],
        'Saturday - 3:00 PM - 6:00 PM' : ['1'],
        'Saturday - 6:00 PM - 9:00 PM' : ['1'],
        'Saturday - 9:00 PM - 12:00 PM' : ['1']
    }
    user_record_2 = survey_data.SurveyData(
        student_id_2, 
        timezone_2, 
        preferred_students_2,
        disliked_students_2, 
        availability_2
        )

    surveys_expected = [
        user_record_1,
        user_record_2
    ]

    # *************************************************************************
    # Read/process the config and survey data
    # *************************************************************************
    
    config_data = read_config.read_config_json("./tests/test_files/configs/config_2.json")
    survey_reader = SurveyDataReader(config_data)
    
    surveys_result = survey_reader.load('./tests/test_files/survey_results/Example_Survey_Results_4.csv')
    

    # *************************************************************************
    # Verify that the config and survey data was read/processed properly.
    # *************************************************************************

    assert(len(surveys_result) == 2) #2 user records
    assert(surveys_result == surveys_expected)