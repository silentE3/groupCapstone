'''
format handles the formatting for data output
'''
from app.group import verify
from app import models
from app.group import validate


class ReportFormatter():
    '''
    formatter for writing reports. Uses the provided configuration
    '''

    def __init__(self, config: models.Configuration) -> None:
        self.data_config = config
        self.report_config = config["report_fields"]

    def format_individual_report(self, groups: list[models.GroupRecord]):
        '''
        formats the grouping information into a format for reporting. Builds the headers into the report
        '''
        records: list[list] = [self.__individual_report_header()]
        verifier = verify.VerifyGrouping(self.data_config)
        user_perfs = verifier.generate_preferred_list_per_user(groups)

        for group in groups:
            for user in group.members:
                record = []
                record.append(user.student_id)

                record.append('')
                if self.report_config['show_disliked_students']:
                    record.append(
                        ';'.join(validate.user_dislikes_group(user, group)))

                record.append(len(user_perfs[user.student_id]) > 0)
                if self.report_config['show_preferred_students']:
                    # for preferred list
                    record.append(";".join(user_perfs[user.student_id]))

                record.append(
                    validate.meets_group_availability_requirement(group))
                if self.report_config['show_availability_overlap']:
                    record.append(
                        ';'.join(validate.group_availability_strings(group)))

                record.append(group.group_id)
                records.append(record)

        return records

    def __individual_report_header(self):
        header = ['Student Id']
        header.append('Meets Dislike Requirement')
        if self.report_config['show_disliked_students']:
            header.append('Disliked students in group')

        header.append('Meets Preferred Goal')
        if self.report_config['show_preferred_students']:
            header.append('Preferred students in group')

        header.append('Meets Availability Requirement')
        if self.report_config['show_availability_overlap']:
            header.append('Availability Overlap')

        header.append('Group Id')

        return header

    def format_group_report(self, groups: list[models.GroupRecord]):
        '''
        returns a 2d array with the group level report of the data.
        '''
        records: list[list] = [self.__group_report_header()]
        verifier = verify.VerifyGrouping(self.data_config)
        group_pairs = verifier.generate_preferred_pairs_per_group(groups)

        for group in groups:
            record = []
            record.append(group.group_id)

            record.append(validate.meets_dislike_requirement(group))
            if self.report_config['show_disliked_students']:
                record.append(
                    ';'.join(validate.users_disliked_in_group(group)))

            pairs = []
            for pair in group_pairs[group.group_id]:
                pairs.append(pair[0] + "/" + pair[1])
            record.append((len(pairs) > 0))
            if self.report_config['show_preferred_students']:
                record.append(';'.join(pairs))
                record.append(len(pairs))

            record.append(
                validate.meets_group_availability_requirement(group))
            if self.report_config['show_availability_overlap']:
                record.append(
                    ';'.join(validate.group_availability_strings(group)))

            records.append(record)

        return records

    def __group_report_header(self) -> list[str]:
        headers = []
        headers.append('Group Id')
        headers.append('Meets Dislike Requirement')
        if self.report_config['show_disliked_students']:
            headers.append('Disliked students in group')

        headers.append('Meets Preferred Goal')
        if self.report_config['show_preferred_students']:
            headers.append('Preferred pairs in group')
            headers.append('Preferred pair count')

        headers.append('Meets Availability Requirement')
        if self.report_config['show_availability_overlap']:
            headers.append('Availability Overlap')

        return headers

    def format_overall_report(self, groups: list[models.GroupRecord]):
        '''
        returns a 2d array with the top level (overall) report data.
        '''
        records: list[list] = [self.__overall_report_header()]

        record = []
        record.append(str(validate.total_disliked_pairings(groups)))
        record.append(str(validate.total_groups_no_availability(groups)))
        record.append(str(validate.total_liked_pairings(groups)))

        records.append(record)

        return records

    def __overall_report_header(self) -> list[str]:
        headers = []
        headers.append('Disliked Pairings')
        headers.append('Number of Groups Without Overlapping Time Slot')
        headers.append('Preferred Pairings')

        return headers
