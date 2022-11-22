'''
Testing Boucher's grouping algorithm
'''
from app import models
from app import config
from app.grouping import boucher
from app.data.load import SurveyDataReader

def test_grouping_algorithm():

    config_data: models.Configuration = config.read_json("./tests/test_files/configs/config_5.json")
    survey_reader = SurveyDataReader(config_data['field_mappings'])
    surveys_result = survey_reader.load('./tests/test_files/survey_results/Example_Survey_Results_5.csv')

    groups: list[models.GroupRecord]
    groups = boucher.create_groups(config_data, surveys_result)

    assert len(groups) == 2
    
