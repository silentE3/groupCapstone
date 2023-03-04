from app.data import reporter
from app import config, models
from app.file import xlsx
from app.group import validate


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
    report_formatter = reporter.ReportFormatter(data_config, {})

    groups = [models.GroupRecord("1", [
        models.SurveyRecord('asurite1', preferred_students=[
            'asurite2', 'asurite3'], disliked_students=['asurite4']),
        models.SurveyRecord('asurite2', preferred_students=[
            'asurite1'], disliked_students=['asurite1']),
        models.SurveyRecord('asurite3', preferred_students=['asurite1']),
        models.SurveyRecord('asurite4', preferred_students=['asurite2'])])
    ]

    report = report_formatter.format_group_report(groups)

    assert report[0] == [xlsx.Cell('Group Id'), xlsx.Cell('Group Size'), xlsx.Cell('Meets Dislike Requirement'), xlsx.Cell('Meets Availability Requirement'),
                         xlsx.Cell('Availability Overlap'), xlsx.Cell('Meets Preferred Goal'), xlsx.Cell('Preferred pairs in group'), xlsx.Cell('Preferred pair count')]


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
    report_formatter = reporter.ReportFormatter(data_config, {})

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

    assert report[0] == [xlsx.Cell('Group Id'), xlsx.Cell('Group Size'), xlsx.Cell('Meets Dislike Requirement'), xlsx.Cell('Disliked students in group'),
                         xlsx.Cell('Meets Availability Requirement'), xlsx.Cell('Meets Preferred Goal'), xlsx.Cell('Disliked pairs in group'), xlsx.Cell('Disliked pair count'), xlsx.Cell('Score')]


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
    report_formatter = reporter.ReportFormatter(data_config, {})

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

    assert report[1][0] == xlsx.Cell('1')


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
    report_formatter = reporter.ReportFormatter(data_config, {})

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

    report = report_formatter.format_individual_report(groups, report_formatter.generate_availability_map(
        groups, models.SurveyData(groups[0].members+groups[1].members, [])))

    assert report[0] == [xlsx.Cell('Student Id'), xlsx.Cell('Group Id'), xlsx.Cell('Filled out Survey'), xlsx.Cell('Disliked Students'), xlsx.Cell('Meets Dislike Requirement'), xlsx.Cell('Disliked students in group'), xlsx.Cell('Meets Availability Requirement'), xlsx.Cell('Availability Overlap'), xlsx.Cell('Preferred Students'),
                         xlsx.Cell('Meets Preferred Goal'), xlsx.Cell('Preferred students in group'), xlsx.Cell(
                             'Supplied Availability in Survey'), xlsx.Cell('Availability overlaps with others'),
                         xlsx.Cell('monday, 0:00 AM - 3:00 AM'), xlsx.Cell('monday, 3:00 AM - 6:00 AM'), xlsx.Cell(
                             'monday, 6:00 AM - 9:00 AM'), xlsx.Cell('monday, 9:00 AM - 12:00 PM'), xlsx.Cell('monday, 12:00 PM - 3:00 PM'),
                         xlsx.Cell('monday, 3:00 PM - 6:00 PM'), xlsx.Cell(
                             'monday, 6:00 PM - 9:00 PM'), xlsx.Cell('monday, 9:00 PM - 12:00 PM'),
                         xlsx.Cell('tuesday, 0:00 AM - 3:00 AM'), xlsx.Cell('tuesday, 3:00 AM - 6:00 AM'), xlsx.Cell(
                             'tuesday, 6:00 AM - 9:00 AM'), xlsx.Cell('tuesday, 9:00 AM - 12:00 PM'), xlsx.Cell('tuesday, 12:00 PM - 3:00 PM'),
                         xlsx.Cell('tuesday, 3:00 PM - 6:00 PM'), xlsx.Cell(
                             'tuesday, 6:00 PM - 9:00 PM'), xlsx.Cell('tuesday, 9:00 PM - 12:00 PM'),
                         xlsx.Cell('wednesday, 0:00 AM - 3:00 AM'), xlsx.Cell('wednesday, 3:00 AM - 6:00 AM'), xlsx.Cell(
                             'wednesday, 6:00 AM - 9:00 AM'), xlsx.Cell('wednesday, 9:00 AM - 12:00 PM'), xlsx.Cell('wednesday, 12:00 PM - 3:00 PM'),
                         xlsx.Cell('wednesday, 3:00 PM - 6:00 PM'), xlsx.Cell(
                             'wednesday, 6:00 PM - 9:00 PM'), xlsx.Cell('wednesday, 9:00 PM - 12:00 PM'),
                         xlsx.Cell('thursday, 0:00 AM - 3:00 AM'), xlsx.Cell('thursday, 3:00 AM - 6:00 AM'), xlsx.Cell(
                             'thursday, 6:00 AM - 9:00 AM'), xlsx.Cell('thursday, 9:00 AM - 12:00 PM'), xlsx.Cell('thursday, 12:00 PM - 3:00 PM'),
                         xlsx.Cell('thursday, 3:00 PM - 6:00 PM'), xlsx.Cell(
                             'thursday, 6:00 PM - 9:00 PM'), xlsx.Cell('thursday, 9:00 PM - 12:00 PM'),
                         xlsx.Cell('friday, 0:00 AM - 3:00 AM'), xlsx.Cell('friday, 3:00 AM - 6:00 AM'), xlsx.Cell(
                             'friday, 6:00 AM - 9:00 AM'), xlsx.Cell('friday, 9:00 AM - 12:00 PM'), xlsx.Cell('friday, 12:00 PM - 3:00 PM'),
                         xlsx.Cell('friday, 3:00 PM - 6:00 PM'), xlsx.Cell(
                             'friday, 6:00 PM - 9:00 PM'), xlsx.Cell('friday, 9:00 PM - 12:00 PM'),
                         xlsx.Cell('saturday, 0:00 AM - 3:00 AM'), xlsx.Cell('saturday, 3:00 AM - 6:00 AM'), xlsx.Cell(
                             'saturday, 6:00 AM - 9:00 AM'), xlsx.Cell('saturday, 9:00 AM - 12:00 PM'), xlsx.Cell('saturday, 12:00 PM - 3:00 PM'),
                         xlsx.Cell('saturday, 3:00 PM - 6:00 PM'), xlsx.Cell(
                             'saturday, 6:00 PM - 9:00 PM'), xlsx.Cell('saturday, 9:00 PM - 12:00 PM'),
                         xlsx.Cell('sunday, 0:00 AM - 3:00 AM'), xlsx.Cell('sunday, 3:00 AM - 6:00 AM'), xlsx.Cell(
                             'sunday, 6:00 AM - 9:00 AM'), xlsx.Cell('sunday, 9:00 AM - 12:00 PM'), xlsx.Cell('sunday, 12:00 PM - 3:00 PM'),
                         xlsx.Cell('sunday, 3:00 PM - 6:00 PM'), xlsx.Cell('sunday, 6:00 PM - 9:00 PM'), xlsx.Cell('sunday, 9:00 PM - 12:00 PM')]


def test_format_individual_report_check_for_cell_format():
    '''
    Test that the individual report formatter correctly 
    assigns the format to the cells in the report that specify it.
    '''
    report_config: models.ReportConfiguration = {
        'show_preferred_students': True,
        'show_disliked_students': True,
        'show_availability_overlap': True,
        'show_scores': True
    }

    data_config: models.Configuration = config.read_json(
        "./tests/test_files/configs/config_1.json")
    data_config["report_fields"] = report_config
    report_formatter = reporter.ReportFormatter(data_config, {'green_bg': "this is a green background"})

    groups = [
        models.GroupRecord('1', [
            models.SurveyRecord('asurite1', preferred_students=[
                'asurite2', 'asurite3'], disliked_students=['asurite4']),
            models.SurveyRecord('asurite2',  availability={
                                report_formatter.data_config['field_mappings']['availability_field_names'][0]: validate.WEEK_DAYS,
                                report_formatter.data_config['field_mappings']['availability_field_names'][1]: validate.WEEK_DAYS,
                                report_formatter.data_config['field_mappings']['availability_field_names'][2]: validate.WEEK_DAYS,
                                report_formatter.data_config['field_mappings']['availability_field_names'][3]: validate.WEEK_DAYS,
                                report_formatter.data_config['field_mappings']['availability_field_names'][4]: validate.WEEK_DAYS,
                                report_formatter.data_config['field_mappings']['availability_field_names'][5]: validate.WEEK_DAYS,
                                report_formatter.data_config['field_mappings']['availability_field_names'][6]: validate.WEEK_DAYS,
                                report_formatter.data_config['field_mappings'][
                                    'availability_field_names'][7]: validate.WEEK_DAYS
                                }),
            models.SurveyRecord(
                'asurite3', preferred_students=['asurite1']),
            models.SurveyRecord('asurite4', preferred_students=['asurite2'])]),
        models.GroupRecord('2', [
            models.SurveyRecord('asurite5'),
            models.SurveyRecord(
                'asurite6', disliked_students=['asurite1']),
            models.SurveyRecord(
                'asurite7', preferred_students=['asurite1']),
            models.SurveyRecord('asurite8', preferred_students=['asurite2'])])
    ]

    report = report_formatter.format_individual_report(groups, report_formatter.generate_availability_map(
        groups, models.SurveyData(groups[0].members+groups[1].members, [])))

    for field in report[1][13:]:
        assert field.cell_format is not "this is a green background"
    
    for field in report[2][13:]:
        assert field.cell_format is "this is a green background"


def test_format_config_flatten_headers():
    data_config: models.Configuration = config.read_json(
        "./tests/test_files/configs/config_1.json")

    rpt = reporter.ReportFormatter(data_config, {})

    # pylance ignore is needed here because we are testing a "private" method and the name gets mangled
    flattened_headers = rpt._ReportFormatter__config_report_headers()  # type: ignore
    expected_headers = ["class_name", "availability_values_delimiter", "student_id_field_name", "timezone_field_name",
                        "preferred_students_field_names", "disliked_students_field_names", "availability_field_names",
                        "target_group_size", "target_plus_one_allowed", "target_minus_one_allowed", "grouping_passes",
                        "show_preferred_students", "show_disliked_students", "show_availability_overlap", "show_scores", "no_survey_group_method"]

    assert flattened_headers == expected_headers


def test_format_config_flatten_data():
    data_config: models.Configuration = config.read_json(
        "./tests/test_files/configs/config_1.json")

    rpt = reporter.ReportFormatter(data_config, {})

    # pylance ignore is needed here because we are testing a "private" method and the name gets mangled
    flattened_data = rpt._ReportFormatter__get_flatten_config_data()  # type: ignore
    expected_data = [['SER401', ',', 'Please select your ASURITE ID',
                      'In what time zone do you live or will you be during the session? Please use UTC so we can match it easier.',
                      'Preferred team member 1', 'Non-preferred student 1',
                      'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]',
                      2, True, True, 2, False, False, False, False, 0],
                     ['', '', '', '', 'Preferred team member 2', 'Non-preferred student 2', 'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]',
                     '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', 'Preferred team member 3', 'Non-preferred student 3',
                      'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]',
                      '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', 'Preferred team member 4', '',
                      'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]',
                      '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', 'Preferred team member 5', '',
                      'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]',
                      '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', '', '',
                      'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]',
                      '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', '', '',
                      'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]',
                      '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', '', '',
                      'Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]',
                      '', '', '', '', '', '', '', '', '']]
    print(flattened_data)
    print(expected_data)
    assert flattened_data == expected_data
