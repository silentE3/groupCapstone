'''
format handles the formatting for data output
'''
from typing import Any
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
    green_bg = xlsx_writer.new_format("green_bg", {"bg_color": "#00FF00"})

    for index, solution in enumerate(solutions):
        formatter = ReportFormatter(
            data_config, cell_formatters={'green_bg': green_bg})
        availability_map = formatter.generate_availability_map(
            solution, survey_data)
        formatted_data = formatter.format_individual_report(
            solution, availability_map)
        group_formatted_report = formatter.format_group_report(solution)
        overall_formatted_report = formatter.format_overall_report(solution)
        xlsx_writer.write_sheet(
            f'individual_report_{str(index + 1)}', formatted_data).autofit()
        xlsx_writer.write_sheet(
            f'group_report_{str(index + 1)}', group_formatted_report).autofit()
        xlsx_writer.write_sheet(
            f'overall_report_{str(index + 1)}', overall_formatted_report).autofit()

    config_sheet = ReportFormatter(data_config, cell_formatters={
                                   'green_bg': green_bg}).format_config_report()
    xlsx_writer.write_sheet('config', config_sheet)
    xlsx_writer.write_sheet(
        'survey_data', xlsx.convert_to_cells(survey_data.raw_rows))

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

    def __init__(self, config: models.Configuration, cell_formatters: dict[str, Any]) -> None:
        self.data_config = config
        self.report_config = config["report_fields"]
        self.formatters = cell_formatters
        self.avail_slot_header_order: list[tuple[str, str]] = []

    def format_individual_report(self, groups: list[models.GroupRecord], availability_map: models.AvailabilityMap):
        '''
        formats the grouping information into a format for reporting. Builds the headers into the report
        '''
        records: list[list[xlsx.Cell]] = [
            self.__individual_report_header(availability_map)]
        user_perfs = validate.generate_preferred_list_per_user(groups)
        for group in groups:
            group_availability_map: models.GroupAvailabilityMap = self.__get_group_availability_map(
                availability_map, group)
            for user in group.members:

                record: list[xlsx.Cell] = []
                record.append(xlsx.Cell(user.student_id))
                record.append(xlsx.Cell(group.group_id))

                record.append(xlsx.Cell(user.provided_survey_data))
                if self.report_config['show_disliked_students']:
                    record.append(xlsx.Cell(';'.join(user.disliked_students)))

                meets_dislike_req: str = str(
                    len(validate.user_dislikes_group(user, group)) == 0)
                if len(user.disliked_students) == 0:
                    meets_dislike_req = 'none provided'
                record.append(xlsx.Cell(meets_dislike_req))
                if self.report_config['show_disliked_students']:
                    record.append(xlsx.Cell(
                        ';'.join(validate.user_dislikes_group(user, group))))

                record.append(
                    xlsx.Cell(str(validate.meets_group_availability_requirement(group))))

                if self.report_config['show_availability_overlap']:
                    record.append(
                        xlsx.Cell(';'.join(validate.group_availability_strings(group))))

                if self.report_config['show_preferred_students']:
                    record.append(xlsx.Cell(";".join(user.preferred_students)))

                meets_preferred_req: str = str(
                    len(user_perfs[user.student_id]) > 0)
                if len(user.preferred_students) == 0:
                    meets_preferred_req = "none provided"
                record.append(xlsx.Cell(meets_preferred_req))

                if self.report_config['show_preferred_students']:
                    # for preferred list
                    record.append(
                        xlsx.Cell(";".join(user_perfs[user.student_id])))

                # calc if user provided any availability
                record.append(xlsx.Cell(user.provided_availability))
                record.append(xlsx.Cell(user.has_matching_availability))

                # color-coded availability
                # NOTE: The complexity here comes from the desire to ouput these values
                #   in the manner that the sponsor is used to seeing (monaday 0 - 3AM, then
                #   monday 3 - 6 AM, then monday 6 - 9 AM, and so on) under typical usage
                #   conditions (where the availability fields are a time range).
                slot_indexing: dict[tuple[str, str], int] = self.__get_avail_slot_indexing(
                    availability_map)
                if user.student_id in group_availability_map.users:
                    user_availability_map = group_availability_map.users[user.student_id]
                    for avail_slot_tuple in self.avail_slot_header_order:
                        cell_formatter = None
                        if user_availability_map[slot_indexing[avail_slot_tuple]]:
                            cell_formatter = self.formatters.get('green_bg')
                        record.append(xlsx.Cell(' ', cell_formatter))

                records.append(record)

        return records

    def __get_avail_slot_indexing(self, availability_map: models.AvailabilityMap) -> dict[tuple[str, str], int]:
        index: int = 0
        result: dict[tuple[str, str], int] = {}
        for availability_field in availability_map.availability_slots:
            for slot in availability_map.availability_slots[availability_field]:
                result[(availability_field, slot)] = index
                index = index + 1
        return result

    def __individual_report_header(self, availability_map: models.AvailabilityMap):
        header = [xlsx.Cell('Student Id')]
        header.append(xlsx.Cell('Group Id'))
        header.append(xlsx.Cell('Filled out Survey'))
        if self.report_config['show_disliked_students']:
            header.append(xlsx.Cell('Disliked Students'))
        header.append(xlsx.Cell('Meets Dislike Requirement'))
        if self.report_config['show_disliked_students']:
            header.append(xlsx.Cell('Disliked students in group'))

        header.append(xlsx.Cell('Meets Availability Requirement'))
        if self.report_config['show_availability_overlap']:
            header.append(xlsx.Cell('Availability Overlap'))

        if self.report_config['show_preferred_students']:
            header.append(xlsx.Cell('Preferred Students'))
        header.append(xlsx.Cell('Meets Preferred Goal'))
        if self.report_config['show_preferred_students']:
            header.append(xlsx.Cell('Preferred students in group'))

        header.append(xlsx.Cell('Supplied Availability in Survey'))
        header.append(xlsx.Cell('Availability overlaps with others'))

        # color-coded availability headers
        # NOTE: The complexity here comes from the desire to ouput these values
        #   in the manner that the sponsor is used to seeing (monaday 0 - 3AM, then
        #   monday 3 - 6 AM, then monday 6 - 9 AM, and so on) under typical usage
        #   conditions (where the availability fields are a time range & slots are days).
        covered_slots: list[str] = []
        for slots_lists in availability_map.availability_slots.values():
            for slot in slots_lists:
                for availability_field in availability_map.availability_slots.keys():
                    if slot not in covered_slots and slot in availability_map.availability_slots[availability_field]:
                        header.append(
                            xlsx.Cell(slot + ', ' + validate.extract_time(availability_field)))
                        self.avail_slot_header_order.append(
                            (availability_field, slot))
                covered_slots.append(slot)

        return header

    def format_group_report(self, groups: list[models.GroupRecord]) -> list[list[xlsx.Cell]]:
        '''
        returns a 2d array with the group level report of the data.
        '''
        records: list[list[xlsx.Cell]] = [self.__group_report_header()]
        group_pairs = validate.generate_preferred_pairs_per_group(groups)

        for group in groups:
            record: list[xlsx.Cell] = []
            record.append(xlsx.Cell(group.group_id))
            record.append(xlsx.Cell(len(group.members)))

            record.append(xlsx.Cell(validate.meets_dislike_requirement(group)))
            if self.report_config['show_disliked_students']:
                record.append(xlsx.Cell(
                    ';'.join(validate.users_disliked_in_group(group))))

            record.append(xlsx.Cell(
                validate.meets_group_availability_requirement(group)))
            if self.report_config['show_availability_overlap']:
                record.append(xlsx.Cell(
                    ';'.join(validate.group_availability_strings(group))))

            pairs = []
            for pair in group_pairs[group.group_id]:
                pairs.append(pair[0] + "/" + pair[1])
            record.append(xlsx.Cell((len(pairs) > 0)))
            if self.report_config['show_preferred_students']:
                record.append(xlsx.Cell(';'.join(pairs)))
                record.append(xlsx.Cell(len(pairs)))

            # Create the pairs of user dislikes
            pairs = []
            for member in group.members:
                dislikes = validate.user_dislikes_group(member, group)
                for dislike in dislikes:
                    pairs.append(member.student_id + "/" + dislike)

            if self.report_config['show_disliked_students']:
                record.append(xlsx.Cell(';'.join(pairs)))
                record.append(xlsx.Cell(len(pairs)))

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
                record.append(xlsx.Cell(scoring.score_individual_group(
                    group, scoring_vars)))

            records.append(record)

        return records

    def __get_group_availability_map(self, availability_map: models.AvailabilityMap, group: models.GroupRecord) -> models.GroupAvailabilityMap:
        for group_map in availability_map.group_availability:
            if group_map.group_id == group.group_id:
                return group_map
        return models.GroupAvailabilityMap('invalid', {})

    def __group_report_header(self) -> list[xlsx.Cell]:
        headers = []
        headers.append(xlsx.Cell('Group Id'))
        headers.append(xlsx.Cell('Group Size'))
        headers.append(xlsx.Cell('Meets Dislike Requirement'))
        if self.report_config['show_disliked_students']:
            headers.append(xlsx.Cell('Disliked students in group'))

        headers.append(xlsx.Cell('Meets Availability Requirement'))
        if self.report_config['show_availability_overlap']:
            headers.append(xlsx.Cell('Availability Overlap'))

        headers.append(xlsx.Cell('Meets Preferred Goal'))
        if self.report_config['show_preferred_students']:
            headers.append(xlsx.Cell('Preferred pairs in group'))
            headers.append(xlsx.Cell('Preferred pair count'))

        if self.report_config['show_disliked_students']:
            headers.append(xlsx.Cell('Disliked pairs in group'))
            headers.append(xlsx.Cell('Disliked pair count'))

        if self.report_config['show_scores']:
            headers.append(xlsx.Cell('Score'))

        return headers

    def format_config_report(self) -> list[list[xlsx.Cell]]:
        '''
        Generates the Excel report data from the config
        Acts to flatten the structure of the config file so that each property has a header
        '''
        records: list[list] = [self.__config_report_headers()]
        records += self.__get_flatten_config_data()
        return xlsx.convert_to_cells(records)

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

        record.append(xlsx.Cell(num_groups_total))
        record.append(xlsx.Cell(num_disliked_pairings))
        record.append(xlsx.Cell(num_groups_no_avail))
        record.append(xlsx.Cell(num_liked_pairings))
        record.append(xlsx.Cell(num_additional_overlap))

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
            record.append(xlsx.Cell(scoring.score_groups(scoring_vars)))
            record.append(xlsx.Cell(
                round(scoring.standard_dev_groups(groups, scoring_vars), 3)))

        records.append(record)

        return records

    def __overall_report_header(self) -> list[xlsx.Cell]:
        headers = []
        headers.append(xlsx.Cell("Number of Groups"))
        headers.append(xlsx.Cell('Disliked Pairings'))
        headers.append(
            xlsx.Cell('Number of Groups Without Overlapping Time Slot'))
        headers.append(xlsx.Cell('Preferred Pairings'))
        headers.append(xlsx.Cell('"Additional" Overlapping Time Slots'))
        if self.report_config['show_scores']:
            headers.append(xlsx.Cell('Score'))
            headers.append(xlsx.Cell('Standard Deviation of Groups'))

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
            user_availability = user.availability.get(slot)
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
            for slot in self.data_config['field_mappings']['availability_field_names']:
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
