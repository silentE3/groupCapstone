'''
format handles the formatting for data output
'''
from app.group import verify
from app import models
from app.group import validate
from app.group import scoring


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

                record.append(
                    validate.meets_group_availability_requirement(group))
                if self.report_config['show_availability_overlap']:
                    record.append(
                        ';'.join(validate.group_availability_strings(group)))

                record.append(len(user_perfs[user.student_id]) > 0)
                if self.report_config['show_preferred_students']:
                    # for preferred list
                    record.append(";".join(user_perfs[user.student_id]))

                record.append(group.group_id)
                records.append(record)

        return records

    def __individual_report_header(self):
        header = ['Student Id']
        header.append('Meets Dislike Requirement')
        if self.report_config['show_disliked_students']:
            header.append('Disliked students in group')

        header.append('Meets Availability Requirement')
        if self.report_config['show_availability_overlap']:
            header.append('Availability Overlap')

        header.append('Meets Preferred Goal')
        if self.report_config['show_preferred_students']:
            header.append('Preferred students in group')

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

            record.append(
                validate.meets_group_availability_requirement(group))
            if self.report_config['show_availability_overlap']:
                record.append(
                    ';'.join(validate.group_availability_strings(group)))

            pairs = []
            for pair in group_pairs[group.group_id]:
                pairs.append(pair[0] + "/" + pair[1])
            record.append((len(pairs) > 0))
            if self.report_config['show_preferred_students']:
                record.append(';'.join(pairs))
                record.append(len(pairs))

            if self.report_config['show_scores']:
                # Note: the first 4 values are "don't care" for individual group scoring
                scoring_vars = models.GroupSetData(group.group_id,
                                                   0, 0, 0, 0,
                                                   self.data_config["target_group_size"],
                                                   len((self.data_config["field_mappings"])[
                                                       "preferred_students_field_names"]),
                                                   sum(len(group.members)
                                                       for group in groups),
                                                   len((self.data_config["field_mappings"])[
                                                       "availability_field_names"]))
                record.append(scoring.score_individual_group(
                    group, scoring_vars))

            records.append(record)

        return records

    def __group_report_header(self) -> list[str]:
        headers = []
        headers.append('Group Id')
        headers.append('Meets Dislike Requirement')
        if self.report_config['show_disliked_students']:
            headers.append('Disliked students in group')

        headers.append('Meets Availability Requirement')
        if self.report_config['show_availability_overlap']:
            headers.append('Availability Overlap')

        headers.append('Meets Preferred Goal')
        if self.report_config['show_preferred_students']:
            headers.append('Preferred pairs in group')
            headers.append('Preferred pair count')

        if self.report_config['show_scores']:
            headers.append('Score')

        return headers

    def format_overall_report(self, groups: list[models.GroupRecord]):
        '''
        returns a 2d array with the top level (overall) report data.
        '''
        records: list[list] = [self.__overall_report_header()]

        record = []

        num_disliked_pairings: int = validate.total_disliked_pairings(groups)
        num_groups_no_avail: int = validate.total_groups_no_availability(
            groups)
        num_liked_pairings: int = validate.total_liked_pairings(groups)
        num_additional_overlap: int = sum(
            # subtract one to get "additional"
            max(validate.availability_overlap_count(group) - 1, 0)
            for group in groups)

        record.append(str(num_disliked_pairings))
        record.append(str(num_groups_no_avail))
        record.append(str(num_liked_pairings))
        record.append(str(num_additional_overlap))

        if self.report_config['show_scores']:
            scoring_vars = models.GroupSetData("solution_1",
                                               num_groups_no_avail,
                                               num_disliked_pairings,
                                               num_liked_pairings,
                                               num_additional_overlap,
                                               self.data_config["target_group_size"],
                                               len((self.data_config["field_mappings"])[
                                                   "preferred_students_field_names"]),
                                               sum(len(group.members)
                                                   for group in groups),
                                               len((self.data_config["field_mappings"])[
                                                   "availability_field_names"]))
            record.append(scoring.score_groups(scoring_vars))

        records.append(record)

        return records

    def __overall_report_header(self) -> list[str]:
        headers = []
        headers.append('Disliked Pairings')
        headers.append('Number of Groups Without Overlapping Time Slot')
        headers.append('Preferred Pairings')
        headers.append('"Additional" Overlapping Time Slots')
        if self.report_config['show_scores']:
            headers.append('Score')

        return headers
