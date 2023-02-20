from app.data import reporter
from app import config, models


def test_format_group_report_check_header():
    '''
    check that the header is set per the config
    '''
    report_config: models.ReportConfiguration = {
        'show_preferred_students': True,
        'show_disliked_students': False,
        'show_availability_overlap': True,
        'show_scores': False
    }

    data_config: models.Configuration = config.read_json(
        "./tests/test_files/configs/config_1.json")
    data_config["report_fields"] = report_config
    report_formatter = reporter.ReportFormatter(data_config)

    groups = [models.GroupRecord("1", [
        models.SurveyRecord('asurite1', preferred_students=[
            'asurite2', 'asurite3'], disliked_students=['asurite4']),
        models.SurveyRecord('asurite2', preferred_students=[
            'asurite1'], disliked_students=['asurite1']),
        models.SurveyRecord('asurite3', preferred_students=['asurite1']),
        models.SurveyRecord('asurite4', preferred_students=['asurite2'])])
    ]

    report = report_formatter.format_group_report(groups)

    assert report[0] == ['Group Id', 'Group Size', 'Meets Dislike Requirement', 'Meets Availability Requirement',
                         'Availability Overlap', 'Meets Preferred Goal', 'Preferred pairs in group', 'Preferred pair count']


def test_format_group_report_check_header_show_disliked():
    '''
    check that the header is set per the config
    '''
    report_config: models.ReportConfiguration = {
        'show_preferred_students': False,
        'show_disliked_students': True,
        'show_availability_overlap': False,
        'show_scores': True
    }

    data_config: models.Configuration = config.read_json(
        "./tests/test_files/configs/config_1.json")
    data_config["report_fields"] = report_config
    report_formatter = reporter.ReportFormatter(data_config)

    groups = [models.GroupRecord("1",
                                 [
                                     models.SurveyRecord('asurite1', preferred_students=[
                                         'asurite2', 'asurite3'], disliked_students=['asurite4']),
                                     models.SurveyRecord('asurite2', preferred_students=[
                                         'asurite1'], disliked_students=['asurite1']),
                                     models.SurveyRecord(
                                         'asurite3', preferred_students=['asurite1']),
                                     models.SurveyRecord(
                                         'asurite4', preferred_students=['asurite2'])
                                 ])
              ]

    report = report_formatter.format_group_report(groups)

    assert report[0] == ['Group Id', 'Group Size', 'Meets Dislike Requirement', 'Disliked students in group',
                         'Meets Availability Requirement', 'Meets Preferred Goal', 'Disliked pairs in group', 'Disliked pair count', 'Score']


def test_format_group_report_check_group():
    report_config: models.ReportConfiguration = {
        'show_preferred_students': False,
        'show_disliked_students': False,
        'show_availability_overlap': False,
        'show_scores': False
    }

    data_config: models.Configuration = config.read_json(
        "./tests/test_files/configs/config_1.json")
    data_config["report_fields"] = report_config
    report_formatter = reporter.ReportFormatter(data_config)

    groups = [models.GroupRecord("1",
                                 [
                                     models.SurveyRecord('asurite1', preferred_students=[
                                         'asurite2', 'asurite3'], disliked_students=['asurite4']),
                                     models.SurveyRecord('asurite2', preferred_students=[
                                         'asurite1'], disliked_students=['asurite1']),
                                     models.SurveyRecord(
                                         'asurite3', preferred_students=['asurite1']),
                                     models.SurveyRecord(
                                         'asurite4', preferred_students=['asurite2'])
                                 ])
              ]

    report = report_formatter.format_group_report(groups)

    assert report[1][0] == '1'


def test_format_individual_report_check_header_all_enabled():
    report_config: models.ReportConfiguration = {
        'show_preferred_students': True,
        'show_disliked_students': True,
        'show_availability_overlap': True,
        'show_scores': True
    }

    data_config: models.Configuration = config.read_json(
        "./tests/test_files/configs/config_1.json")
    data_config["report_fields"] = report_config
    report_formatter = reporter.ReportFormatter(data_config)

    groups = [
        models.GroupRecord('1', [
            models.SurveyRecord('asurite1', preferred_students=[
                'asurite2', 'asurite3'], disliked_students=['asurite4']),
            models.SurveyRecord('asurite2', preferred_students=[
                'asurite1'], disliked_students=['asurite1']),
            models.SurveyRecord(
                'asurite3', preferred_students=['asurite1']),
            models.SurveyRecord('asurite4', preferred_students=['asurite2'])]),
        models.GroupRecord('2', [
            models.SurveyRecord('asurite5', preferred_students=[
                'asurite6'], disliked_students=['asurite7']),
            models.SurveyRecord(
                'asurite6', disliked_students=['asurite1']),
            models.SurveyRecord(
                'asurite7', preferred_students=['asurite1']),
            models.SurveyRecord('asurite8', preferred_students=['asurite2'])])
    ]

    report = report_formatter.format_individual_report(groups)

    assert report[0] == ['Student Id', 'Disliked Students', 'Meets Dislike Requirement', 'Disliked students in group', 'Availability', 'Meets Availability Requirement', 'Availability Overlap', 'Preferred Students',
                         'Meets Preferred Goal', 'Preferred students in group', 'Supplied Availability in Survey', 'Availability overlaps with others',
                         'Group Id']


def test_format_config_flatten_headers():
    data_config: models.Configuration = config.read_json(
        "./tests/test_files/configs/config_1.json")
    
    rpt = reporter.ReportFormatter(data_config)
    
    #pylance ignore is needed here because we are testing a "private" method and the name gets mangled
    flattened_headers = rpt._ReportFormatter__config_report_headers() # type: ignore 
    expected_headers = ["class_name", "availability_values_delimiter", "student_id_field_name", "timezone_field_name", 
                        "preferred_students_field_names", "disliked_students_field_names", "availability_field_names", 
                        "target_group_size", "target_plus_one_allowed", "target_minus_one_allowed", "grouping_passes",
                        "show_preferred_students", "show_disliked_students", "show_availability_overlap", "show_scores"]

    assert flattened_headers == expected_headers                    

def test_format_config_flatten_data():
    data_config: models.Configuration = config.read_json(
        "./tests/test_files/configs/config_1.json")
    
    rpt = reporter.ReportFormatter(data_config)
    
    #pylance ignore is needed here because we are testing a "private" method and the name gets mangled
    flattened_data = rpt._ReportFormatter__get_flatten_config_data() # type: ignore 
    expected_data = [['SER401', ',', 'Please select your ASURITE ID', 
                    'In what time zone do you live or will you be during the session? Please use UTC so we can match it easier.', 
                    'Preferred team member 1', 'Non-preferred student 1', 
                    'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]', 
                    2, True, True, 2, False, False, False, False], ['', '', '', '', 'Preferred team member 2', 'Non-preferred student 2', 
                    'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]', 
                    '', '', '', '', '', '', '', ''], ['', '', '', '', 'Preferred team member 3', 'Non-preferred student 3', 
                    'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]', 
                    '', '', '', '', '', '', '', ''], ['', '', '', '', 'Preferred team member 4', '', 
                    'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]', 
                    '', '', '', '', '', '', '', ''], ['', '', '', '', 'Preferred team member 5', '', 
                    'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]', 
                    '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', 
                    'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]', 
                    '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', 
                    'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]', 
                    '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', 
                    'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]', 
                    '', '', '', '', '', '', '', '']]

    assert flattened_data == expected_data    