'''
Unit tests for Verify functionality
'''
from app.data import load
from app import config, models, core
from app.grouping import randomizer
from app.group import verify


def test_all_users_are_grouped():
    '''
    This test asserts that all users have been grouped
    '''
    # load the config data
    config_data: models.Configuration = config.read_json("./tests/test_files/configs/config_1_full.json")

    # load the survey data
    survey_reader = load.SurveyDataReader(config_data['field_mappings'])
    surveys_result = survey_reader.load('./tests/test_files/survey_results/Example_Survey_Results_1_full.csv')

    # get the number of groups and create a list of groups
    num_groups = core.get_num_groups(surveys_result, config_data["target_group_size"])
    grouper = randomizer.RandomGrouper()
    groupings = grouper.create_groups(surveys_result, config_data["target_group_size"], num_groups)
    
    # verify that all users have been grouped
    verifier = verify.VerifyGrouping(config_data)
    ungrouped = verifier.verify_all_users_grouped(surveys_result, groupings)

    assert len(ungrouped) == 0

    # remove a users from one of the groups and test again
    groupings[0].members.pop()

    ungrouped = verifier.verify_all_users_grouped(surveys_result, groupings)

    assert len(ungrouped) == 1