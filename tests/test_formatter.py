from app.data import formatter, generate
from app import models


def test_format_group_report_check_header():
    '''
    check that the header is set per the config
    '''
    config: models.ReportConfiguration = {
        'show_preferred_students': True,
        'show_disliked_students': False,
        'show_availability_overlap': True,
    }

    report_formatter = formatter.ReportFormatter(config)

    groups = [models.GroupRecord("1", [
        models.SurveyRecord('asurite1', preferred_students=[
            'asurite2', 'asurite3'], disliked_students=['asurite4']),
        models.SurveyRecord('asurite2', preferred_students=[
            'asurite1'], disliked_students=['asurite1']),
        models.SurveyRecord('asurite3', preferred_students=['asurite1']),
        models.SurveyRecord('asurite4', preferred_students=['asurite2'])])
    ]

    report = report_formatter.format_group_report(groups)

    assert report[0] == ['Group Id', 'Meets Dislike Requirement', 'Meets Preferred Requirement', 'Preferred students in group',
                         'Meets Availability Requirement', 'Availability Overlap']


def test_format_group_report_check_header_show_disliked():
    '''
    check that the header is set per the config
    '''
    config: models.ReportConfiguration = {
        'show_preferred_students': False,
        'show_disliked_students': True,
        'show_availability_overlap': False,
    }

    report_formatter = formatter.ReportFormatter(config)

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

    assert report[0] == ['Group Id', 'Meets Dislike Requirement', 'Disliked students in group', 'Meets Preferred Requirement',
                         'Meets Availability Requirement']


def test_format_group_report_check_group():
    config: models.ReportConfiguration = {
        'show_preferred_students': False,
        'show_disliked_students': False,
        'show_availability_overlap': False,
    }

    report_formatter = formatter.ReportFormatter(config)

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

    assert report[1][0] == 0


def test_format_individual_report_check_header_all_enabled():
    config: models.ReportConfiguration = {
        'show_preferred_students': True,
        'show_disliked_students': True,
        'show_availability_overlap': True,
    }

    report_formatter = formatter.ReportFormatter(config)

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

    assert report[0] == ['Student Id', 'Meets Dislike Requirement', 'Disliked students in group',
                         'Meets Preferred Requirement', 'Preferred students in group', 'Meets Availability Requirement', 'Availability Overlap', 'Group Id']
