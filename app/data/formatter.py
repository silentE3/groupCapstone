'''
format handles the formatting for data output
'''
from app import models
from app.group import validate


class ReportFormatter():
    '''
    formatter for writing reports. Uses the provided configuration
    '''

    def __init__(self, config: models.ReportConfiguration) -> None:
        self.config = config

    def format_individual_report(self, groups: list[models.GroupRecord]):
        '''
        formats the grouping information into a format for reporting. Builds the headers into the report
        '''
        records: list[list] = [self.__individual_report_header()]
        for group in groups:
            for user in group.members:
                record = []
                record.append(user.student_id)

                record.append('')
                if self.config['show_disliked_students']:
                    record.append(
                        ';'.join(validate.user_dislikes_group(user, group.members)))

                record.append('')
                if self.config['show_preferred_students']:
                    record.append('')

                record.append('')
                if self.config['show_availability_overlap']:
                    record.append('')

                record.append(groups.index(group))
                records.append(record)

        return records

    def __individual_report_header(self):
        header = ['Student Id']
        header.append('Meets Dislike Requirement')
        if self.config['show_disliked_students']:
            header.append('Disliked students in group')

        header.append('Meets Preferred Requirement')
        if self.config['show_preferred_students']:
            header.append('Preferred students in group')

        header.append('Meets Availability Requirement')
        if self.config['show_availability_overlap']:
            header.append('Availability Overlap')

        header.append('Group Id')

        return header

    def format_group_report(self, groups: list[models.GroupRecord]):
        '''
        returns a 2d array with the group level report of the data.
        '''
        records: list[list] = [self.__group_report_header()]
        for idx, group in enumerate(groups):
            record = []
            record.append(idx)

            record.append(validate.meets_dislike_requirement(group.members))
            if self.config['show_disliked_students']:
                record.append('')

            record.append('')
            if self.config['show_preferred_students']:
                record.append('')

            record.append(
                validate.meets_group_availability_requirement(group.members))
            if self.config['show_availability_overlap']:
                record.append('')

            records.append(record)

        return records

    def __group_report_header(self) -> list[str]:
        headers = []
        headers.append('Group Id')
        headers.append('Meets Dislike Requirement')
        if self.config['show_disliked_students']:
            headers.append('Disliked students in group')

        headers.append('Meets Preferred Requirement')
        if self.config['show_preferred_students']:
            headers.append('Preferred students in group')

        headers.append('Meets Availability Requirement')
        if self.config['show_availability_overlap']:
            headers.append('Availability Overlap')

        return headers
