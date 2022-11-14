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

def test_generate_preferred_pairs_per_group():
    '''
    Generates a test grouping and runs generate_preferred_pairs_per_group against it
    then compairs the user lists
    '''

    # load the config data. Does not matter what config data is used
    config_data: models.Configuration = config.read_json("./tests/test_files/configs/config_1_full.json")

    group1 = models.GroupRecord("1", 
        [models.SurveyRecord("a1", "", "", "", "", ["a2", "a3"], [], {}), 
        models.SurveyRecord("a2", "", "", "", "", ["a1", "a3"], [], {}),
        models.SurveyRecord("a3", "", "", "", "", ["a1", "a2"], [], {})])
    
    
    group2 = models.GroupRecord("2", 
        [models.SurveyRecord("a4", "", "", "", "", ["a5"], [], {}), 
        models.SurveyRecord("a5", "", "", "", "", ["a6", "a8"], [], {}),
        models.SurveyRecord("a6", "", "", "", "", ["a7"], [], {})])

    verifier = verify.VerifyGrouping(config_data)
    perfs = verifier.generate_preferred_pairs_per_group([group1, group2])

    # check the lengths of the preferred pairings for a group
    assert len(perfs["1"]) == 6
    assert len(perfs["2"]) == 2
    
def test_generate_preferred_list_per_user():
    '''
    Generates a test group and runs generate_preferred_list_per_user against it
    then compairs the user lists
    '''

    # load the config data. Does not matter what config data is used
    config_data: models.Configuration = config.read_json("./tests/test_files/configs/config_1_full.json")

    group1 = models.GroupRecord("1", 
        [models.SurveyRecord("a1", "", "", "", "", ["a2", "a3"], [], {}), 
        models.SurveyRecord("a2", "", "", "", "", ["a1", "a3"], [], {}),
        models.SurveyRecord("a3", "", "", "", "", ["a1", "a2"], [], {})])
    
    
    group2 = models.GroupRecord("2", 
        [models.SurveyRecord("a4", "", "", "", "", ["a5"], [], {}), 
        models.SurveyRecord("a5", "", "", "", "", ["a6", "a8"], [], {}),
        models.SurveyRecord("a6", "", "", "", "", ["a7"], [], {})])

    verifier = verify.VerifyGrouping(config_data)
    perfs = verifier.generate_preferred_list_per_user([group1, group2])

    # check the lengths of the preferred users per user
    assert len(perfs["a1"]) == 2 
    assert len(perfs["a2"]) == 2 
    assert len(perfs["a3"]) == 2 
    assert len(perfs["a4"]) == 1 
    assert len(perfs["a5"]) == 1 
    assert len(perfs["a6"]) == 0 