'''
format handles the formatting for data output
'''
from app import models
from app.group import validate
from app.group import scoring
from app.file import xlsx
from app import config as cfg


def write_report(solutions: list[list[models.GroupRecord]], survey_data: models.SurveyData, data_config: models.Configuration, filename: str):
    '''
    writes the report to an xlsx file
    '''
    xlsx_writer = xlsx.XLSXWriter(filename)

    for index, solution in enumerate(solutions):
        formatter = ReportFormatter(data_config)
        formatted_data = formatter.format_individual_report(solution)
        group_formatted_report = formatter.format_group_report(solution)
        overall_formatted_report = formatter.format_overall_report(solution)
        availability_map = formatter.generate_availability_map(
            solution, survey_data)
        # pylint: disable-fixme
        # TODO: Placeholder for availability reporting. Can remove the preceding pylint: disable when done
        xlsx_writer.write_sheet('availability_report_' + str(index + 1), [list(availability_map.availability_slots.keys())])
        xlsx_writer.write_sheet('individual_report_' +
                                str(index + 1), formatted_data)
        xlsx_writer.write_sheet(
            'group_report_' + str(index + 1), group_formatted_report)
        xlsx_writer.write_sheet(
            'overall_report_' + str(index + 1), overall_formatted_report)

    config_sheet = ReportFormatter(data_config).format_config_report()
    xlsx_writer.write_sheet('config', config_sheet)

    xlsx_writer.write_sheet('survey_data', survey_data.raw_rows)

    xlsx_writer.save()


def get_user_availability(user: models.SurveyRecord):
    '''
    This method gets a user's availability and formats it for excel file.
    '''
    available_slots: list[str] = []
    for time_slot, availability_days in user.availability.items():
        for day in availability_days:
            available_slots.append(
                day + " @ " + validate.extract_time(time_slot))

    return available_slots


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
        user_perfs = validate.generate_preferred_list_per_user(groups)

        for group in groups:
            for user in group.members:

                record = []
                record.append(user.student_id)

                record.append(';'.join(user.disliked_students))

                if len(user.disliked_students) == 0:
                    record.append('none provided')
                else:
                    record.append(
                        len(validate.user_dislikes_group(user, group)) == 0)
                if self.report_config['show_disliked_students']:
                    record.append(
                        ';'.join(validate.user_dislikes_group(user, group)))

                record.append(';'.join(get_user_availability(user)))

                record.append(
                    validate.meets_group_availability_requirement(group))
                if self.report_config['show_availability_overlap']:
                    record.append(
                        ';'.join(validate.group_availability_strings(group)))

                record.append(";".join(user.preferred_students))

                if len(user.preferred_students) == 0:
                    record.append("none provided")
                else:
                    record.append(len(user_perfs[user.student_id]) > 0)

                if self.report_config['show_preferred_students']:
                    # for preferred list
                    record.append(";".join(user_perfs[user.student_id]))

                # calc if user provided any availability
                record.append(str(user.provided_availability))
                record.append(str(user.has_matching_availability))

                record.append(group.group_id)
                records.append(record)

        return records

    def __individual_report_header(self):
        header = ['Student Id']
        header.append('Disliked Students')
        header.append('Meets Dislike Requirement')
        if self.report_config['show_disliked_students']:
            header.append('Disliked students in group')

        header.append('Availability')
        header.append('Meets Availability Requirement')
        if self.report_config['show_availability_overlap']:
            header.append('Availability Overlap')

        header.append('Preferred Students')
        header.append('Meets Preferred Goal')
        if self.report_config['show_preferred_students']:
            header.append('Preferred students in group')

        header.append('Supplied Availability in Survey')
        header.append('Availability overlaps with others')

        header.append('Group Id')

        return header

    def format_group_report(self, groups: list[models.GroupRecord]):
        '''
        returns a 2d array with the group level report of the data.
        '''
        records: list[list] = [self.__group_report_header()]
        group_pairs = validate.generate_preferred_pairs_per_group(groups)

        for group in groups:
            record = []
            record.append(group.group_id)
            record.append(len(group.members))

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

            # Create the pairs of user dislikes
            pairs = []
            for member in group.members:
                dislikes = validate.user_dislikes_group(member, group)
                for dislike in dislikes:
                    pairs.append(member.student_id + "/" + dislike)

            if self.report_config['show_disliked_students']:
                record.append(';'.join(pairs))
                record.append(len(pairs))

            if self.report_config['show_scores']:
                # Note: the first 4 values are "don't care" for individual group scoring
                scoring_vars = models.GroupSetData(group.group_id,
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
        headers.append('Group Size')
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

        if self.report_config['show_disliked_students']:
            headers.append('Disliked pairs in group')
            headers.append('Disliked pair count')

        if self.report_config['show_scores']:
            headers.append('Score')

        return headers

    def format_config_report(self) -> list[list]:
        '''
        Generates the Excel report data from the config
        Acts to flatten the structure of the config file so that each property has a header
        '''
        records: list[list] = [self.__config_report_headers()]
        records += self.__get_flatten_config_data()
        return records

    def __get_config_data(self, data: dict) -> list[object]:
        '''
        Recursively generates a list of all data from the config file
        turning it into a flat 1d list of data
        '''
        values = []

        for item in data:
            if isinstance(data[item], dict):
                values += self.__get_config_data(dict(data[item]))
            else:
                values.append(data[item])

        return values

    def __get_list_entries(self, data: list[object]) -> dict[int, list]:
        '''
        Creates a dictionary of the list data types in the flat data list
        with their index in the data list as the key
        '''

        lists: dict[int, list] = {}

        for index, item in enumerate(data):
            if isinstance(item, list):
                lists[index] = list(item)

        return lists

    def __get_max_list_length(self, data: list[object]) -> int:
        '''
        Finds all list data types in the flat data list and returns the max size
        '''
        max_len: int = 0

        for item in data:
            if isinstance(item, list) and len(list(item)) > max_len:
                max_len = len(list(item))

        return max_len

    def __create_blank_2d_list(self, dim1: int, dim2: int) -> list[list]:
        '''
        Creates a 2d list filled with empty strings
        '''
        sheet: list[list] = []
        for _ in range(dim1):
            line: list = [""] * dim2
            sheet.append(line)

        return sheet

    def __get_flatten_config_data(self) -> list[list]:
        '''
        Turns the hierarchical config data structure into a two-dimensional array of values
        '''
        data: list[object] = self.__get_config_data(dict(cfg.CONFIG_DATA))
        lists: dict[int, list] = self.__get_list_entries(data)
        max_len: int = self.__get_max_list_length(data)
        flattened_data: list[list] = self.__create_blank_2d_list(
            max_len, len(data))

        for index, item in enumerate(data):
            if not isinstance(item, list):
                flattened_data[0][index] = item

        for key, value in lists.items():
            for index, val in enumerate(value):
                flattened_data[index][key] = val

        return flattened_data

    def __get_config_headers(self, data: dict) -> list[str]:
        '''
        Recursively generates a list of all headers from the config file
        '''
        headers = []

        for item in data:
            if isinstance(data[item], dict):
                headers += self.__get_config_headers(dict(data[item]))
            else:
                headers.append(item)

        return headers

    def __config_report_headers(self) -> list[str]:
        '''
        Creates the list of headers based off of the config file
        '''
        return self.__get_config_headers(dict(cfg.CONFIG_DATA))

    def format_overall_report(self, groups: list[models.GroupRecord]):
        '''
        returns a 2d array with the top level (overall) report data.
        '''
        records: list[list] = [self.__overall_report_header()]

        record = []

        num_groups_total: int = len(groups)
        num_disliked_pairings: int = validate.total_disliked_pairings(groups)
        num_groups_no_avail: int = validate.total_groups_no_availability(
            groups)
        num_liked_pairings: int = validate.total_liked_pairings(groups)
        num_additional_overlap: int = sum(
            # subtract one to get "additional"
            max(validate.availability_overlap_count(group) - 1, 0)
            for group in groups)

        record.append(str(num_groups_total))
        record.append(str(num_disliked_pairings))
        record.append(str(num_groups_no_avail))
        record.append(str(num_liked_pairings))
        record.append(str(num_additional_overlap))

        if self.report_config['show_scores']:
            scoring_vars = models.GroupSetData("solution_1",
                                               self.data_config["target_group_size"],
                                               len((self.data_config["field_mappings"])[
                                                   "preferred_students_field_names"]),
                                               sum(len(group.members)
                                                   for group in groups),
                                               len((self.data_config["field_mappings"])[
                                                   "availability_field_names"]),
                                               num_groups_no_avail,
                                               num_disliked_pairings,
                                               num_liked_pairings,
                                               num_additional_overlap)
            record.append(scoring.score_groups(scoring_vars))
            record.append(
                round(scoring.standard_dev_groups(groups, scoring_vars), 3))

        records.append(record)

        return records

    def __overall_report_header(self) -> list[str]:
        headers = []
        headers.append("Number of Groups")
        headers.append('Disliked Pairings')
        headers.append('Number of Groups Without Overlapping Time Slot')
        headers.append('Preferred Pairings')
        headers.append('"Additional" Overlapping Time Slots')
        if self.report_config['show_scores']:
            headers.append('Score')
            headers.append('Standard Deviation of Groups')

        return headers

    def generate_availability_map(self, data: list[models.GroupRecord], survey_data: models.SurveyData) -> models.AvailabilityMap:
        '''
        Generates the availability map per group, per user, per availability slot
        '''
        availability_map = models.AvailabilityMap(
            self.__generate_availability_slot_map(survey_data), [])
        # first create the map of groups with members
        for group in data:
            group_availability = models.GroupAvailabilityMap(
                group.group_id, {})
            for user in group.members:
                group_availability.users[user.student_id] = self.__generate_user_availability_list(
                    user, availability_map)

            availability_map.group_availability.append(group_availability)

        return availability_map

    def __generate_user_availability_list(self, user: models.SurveyRecord, slot_map: models.AvailabilityMap) -> list[bool]:
        '''
        given a user and the map of availability slots, a list of 
        bools are created that indicated the time slots available.

        map:

        [....availability slot....][....availability slot....]
        [day1][day2][day3]...[day7][day1][day2][day3]...[day7]
          .     .     .        .     .     .     .        .       
          .     .     .        .     .     .     .        .
        list of bools for user:.     .     .     .        .
          .     .     .        .     .     .     .        .
        [bool][bool][bool]...[bool][bool][bool][bool]...[bool]

        '''
        availability: list[bool] = []

        for slot in slot_map.availability_slots:
            # first see if the user has that slot
            user_availability = user.availability[slot]
            # if they do, add bools to the availability list
            if user_availability:
                for time in slot_map.availability_slots[slot]:
                    availability.append(time in user_availability)
            # else just add a bunch of False values to the list
            # equal to the size of the times in the slot
            else:
                availability.extend(
                    [False] * len(slot_map.availability_slots[slot]))

        return availability

    def __are_time_slots_days(self, survey_data: models.SurveyData) -> bool:
        '''
        Scans all user availability slots. If all are day-name values, returns true
        '''
        for users in survey_data.records:
            for slot_val in users.availability.values():
                for time in slot_val:
                    if time not in validate.WEEK_DAYS:
                        return False
        return True

    # NOTE: this method may not need to check each user if we can assume a fixed set of days for each time slot
    def __generate_availability_slot_map(self, survey_data: models.SurveyData) -> dict[str, list[str]]:
        '''
        Creates a dictionary of all current slots across all users
        '''
        slot_map: dict[str, list[str]] = {}

        # if we are sure the time slots are day-names, then just fill with the day names
        if self.__are_time_slots_days(survey_data):
            for slot in cfg.CONFIG_DATA['field_mappings']['availability_field_names']:
                slot_map[slot] = validate.WEEK_DAYS

            return slot_map

        for survey in survey_data.records:
            for slot in survey.availability:
                # pylint: disable=consider-iterating-dictionary
                if slot not in slot_map.keys():
                    slot_map[slot] = []
                slot_map[slot] = list(set(slot_map[slot])
                                      | set(survey.availability[slot]))

        return slot_map
