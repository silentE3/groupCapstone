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

    assert report[0] == ['Student Id', 'Meets Dislike Requirement', 'Disliked students in group','Availability', 'Meets Availability Requirement', 'Availability Overlap', 'Preferred Students'
                         'Meets Preferred Goal', 'Preferred students in group', 'Supplied Availability in Survey', 'Availability overlaps with others', 
                         'Group Id']
