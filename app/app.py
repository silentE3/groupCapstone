'''
app holds the class for setting up the application
'''

from abc import abstractmethod
from app import models
from app.file import xlsx
from app import core, output
from app.data import formatter, load
from app.group import verify


class AbstractGrouper:
    '''
    provides the abstract class for grouping. This should be used when implementing the grouping algorithm
    '''
    @abstractmethod
    def create_groups(self,
                      survey_data: list,
                      target_group_size: int,
                      num_groups: int) -> list[models.GroupRecord]:
        '''
        method to generate groups given the criteria and
        '''


class Application():
    '''
    Application holds the main operations for the grouping tool.
    '''

    def __init__(self, config: models.Configuration, grouper: AbstractGrouper) -> None:
        self.__config = config
        self.__report_formatter = formatter.ReportFormatter(
            config["report_fields"])
        self.__survey_reader = load.SurveyDataReader(config["field_mappings"])
        self.__group_reader = load.GroupingDataReader()
        self.__grouper = grouper
        self.__verifier = verify.VerifyGrouping(config)

    def read_survey(self, filename: str) -> list[models.SurveyRecord]:
        '''
        reads the survey data into a list of records
        '''
        return self.__survey_reader.load(filename)

    def read_groups(self, filename: str) -> list[models.GroupRecord]:
        '''
        reads the groups into a list of group records
        '''
        return self.__group_reader.load(filename)

    def group_students(self, records: list[models.SurveyRecord]):
        '''
        performs the grouping of the survey data
        '''
        # Perform pre-grouping error checking
        if core.pre_group_error_checking(self.__config["target_group_size"], records):
            raise Exception("")  # error found -- don't continue

        # Determine number of groups
        num_groups: int = core.get_num_groups(
            records, self.__config["target_group_size"])

        if num_groups < 0:
            raise Exception('''
**********************
Error: Not possible to adhere to the target_group_size (+/- 1) defined in the config file (config.json) in use.
**********************
'''
                            )

        # Create random groupings
        groups: list[models.GroupRecord] = self.__grouper.create_groups(
            records, self.__config["target_group_size"], num_groups)

        return groups

    def verify_groups(self, records: list[models.SurveyRecord], groups: list[models.GroupRecord], filename: str):
        '''
        uses the verifier to "verify" the groups
        '''
        self.__verifier.verify(records, groups, filename)

    def write_groups(self, groups: list[models.GroupRecord], filename: str):
        '''
        writes the groups to an output file
        '''
        output.GroupingDataWriter(
            self.__config).write_csv(groups, filename)

    def write_report(self, groups: list[models.GroupRecord], filename: str):
        '''
        writes out the grouping report
        '''
        formatted_data = self.__report_formatter.format_individual_report(
            groups)
        group_formatted_report = self.__report_formatter.format_group_report(
            groups)
        overall_formatted_report = self.__report_formatter.format_overall_report(
            groups)
        xlsx_writer = xlsx.XLSXWriter(filename)
        xlsx_writer.write_sheet('individual_report', formatted_data)
        xlsx_writer.write_sheet('group_report', group_formatted_report)
        xlsx_writer.write_sheet('overall_report', overall_formatted_report)
        xlsx_writer.save()
