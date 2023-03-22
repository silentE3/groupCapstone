from app import config
from app import models
from app.grouping import grouper_2, printer

# At this time, these tests only verify the portions of grouper_2 that are related to accomadating
#  the variable group sizing margins, which was implemented via Taiga task #171. This includes
#  unit testing of the following functions in grouper_2:
#       - balance_groups
#       - balance_group
# Note: Per add_student_to_group, a group should never have more students than allowed. For this reason,
#  the balance_groups function only handles fixing groups with LESS members than allowed.

configuration: models.Configuration = config.read_json(
    './tests/test_files/configs/config_1.json')


def __initialize_students(num_students: int) -> list[models.SurveyRecord]:
    students = []
    for i in range(0, num_students):
        student = models.SurveyRecord(
            student_id=str(i + 1),
            preferred_students=[],
            disliked_students=[],
            availability={"1": []})
        students.append(student)
    return students


def test_balance_groups_all_start_balanced_1(capfd):
    '''
    This test verifies the balance_groups function for the situation where:
        - groups smaller than target group size are NOT allowed
        - groups larger than target group size are NOT allowed
        - all groups are already within the allowable limits
    Expected result: Nothing (no balancing) occurs
    '''
    students = __initialize_students(10)

    configuration["target_group_size"] = 5
    configuration["target_minus_one_allowed"] = False
    configuration["target_plus_one_allowed"] = False
    group_count: int = 2

    group_1: models.GroupRecord = models.GroupRecord("1", students[0:5])
    group_2: models.GroupRecord = models.GroupRecord("2", students[5:10])

    grouper2 = grouper_2.Grouper2(
        students, configuration, 2, printer.GroupingConsolePrinter())
    grouper2.groups = [group_1, group_2]
    assert len(group_1.members) == 5
    assert len(group_2.members) == 5

    grouper2.balance_groups()
    out, err = capfd.readouterr()

    assert out == ""
    assert len(group_1.members) == 5
    assert len(group_2.members) == 5


def test_balance_groups_all_start_balanced_2(capfd):
    '''
    This test verifies the balance_groups function for the situation where:
        - groups smaller than target group size are allowed
        - groups larger than target group size are NOT allowed
        - all groups are already within the allowable limits
    Expected result: Nothing (no balancing) occurs
    '''
    students = __initialize_students(7)

    configuration["target_group_size"] = 4
    configuration["target_minus_one_allowed"] = True
    configuration["target_plus_one_allowed"] = False
    group_count: int = 2

    group_1: models.GroupRecord = models.GroupRecord("1", students[0:3])
    group_2: models.GroupRecord = models.GroupRecord("2", students[3:7])

    grouper2 = grouper_2.Grouper2(
        students, configuration, 2, printer.GroupingConsolePrinter())
    grouper2.groups = [group_1, group_2]
    assert len(group_1.members) == 3
    assert len(group_2.members) == 4

    grouper2.balance_groups()
    out, err = capfd.readouterr()

    assert out == ""
    assert len(group_1.members) == 3
    assert len(group_2.members) == 4


def test_balance_groups_all_start_balanced_3(capfd):
    '''
    This test verifies the balance_groups function for the situation where:
        - groups smaller than target group size are NOT allowed
        - groups larger than target group size are allowed
        - all groups are already within the allowable limits
    Expected result: Nothing (no balancing) occurs
    '''
    students = __initialize_students(9)

    configuration["target_group_size"] = 4
    configuration["target_minus_one_allowed"] = True
    configuration["target_plus_one_allowed"] = False
    group_count: int = 2

    group_1: models.GroupRecord = models.GroupRecord("1", students[0:4])
    group_2: models.GroupRecord = models.GroupRecord("2", students[4:9])

    grouper2 = grouper_2.Grouper2(
        students, configuration, 2, printer.GroupingConsolePrinter())
    grouper2.groups = [group_1, group_2]
    assert len(group_1.members) == 4
    assert len(group_2.members) == 5

    grouper2.balance_groups()
    out, err = capfd.readouterr()

    assert out == ""
    assert len(group_1.members) == 4
    assert len(group_2.members) == 5


def test_balance_groups_all_start_balanced_4(capfd):
    '''
    This test verifies the balance_groups function for the situation where:
        - groups smaller than target group size are allowed
        - groups larger than target group size are allowed
        - all groups are already within the allowable limits
    Expected result: Nothing (no balancing) occurs
    '''
    students = __initialize_students(10)

    configuration["target_group_size"] = 5
    configuration["target_minus_one_allowed"] = True
    configuration["target_plus_one_allowed"] = False
    group_count: int = 2

    group_1: models.GroupRecord = models.GroupRecord("1", students[0:4])
    group_2: models.GroupRecord = models.GroupRecord("2", students[4:10])

    grouper2 = grouper_2.Grouper2(
        students, configuration, 2, printer.GroupingConsolePrinter())
    grouper2.groups = [group_1, group_2]
    assert len(group_1.members) == 4
    assert len(group_2.members) == 6

    grouper2.balance_groups()
    out, err = capfd.readouterr()

    assert out == ""
    assert len(group_1.members) == 4
    assert len(group_2.members) == 6


def test_balance_groups_start_unbalanced_1(capfd):
    '''
    This test verifies the balance_groups and balance_group functions for the situation where:
        - groups smaller than target group size are NOT allowed
        - groups larger than target group size are NOT allowed
        - group 1 one student lower than allowable limit
        - group 2 one student higher than allowable limit
    Expected result: both groups are balanced to the target.
    '''
    students = __initialize_students(10)

    configuration["target_group_size"] = 5
    configuration["target_minus_one_allowed"] = False
    configuration["target_plus_one_allowed"] = False
    group_count: int = 2

    group_1: models.GroupRecord = models.GroupRecord("1", students[0:4])
    group_2: models.GroupRecord = models.GroupRecord("2", students[4:10])

    grouper2 = grouper_2.Grouper2(
        students, configuration, 2, printer.GroupingConsolePrinter())
    grouper2.groups = [group_1, group_2]
    assert len(group_1.members) == 4
    assert len(group_2.members) == 6

    grouper2.balance_groups()
    out, err = capfd.readouterr()

    assert ('balancing group: 1 with size 4') in out
    assert len(group_1.members) == 5
    assert len(group_2.members) == 5


def test_balance_groups_start_unbalanced_2(capfd):
    '''
    This test verifies the balance_groups and balance_group functions for the situation where:
        - groups smaller than target group size are allowed
        - groups larger than target group size are NOT allowed
        - group 1 one student lower than allowable limit
        - group 2 at the target (one higher than the lower limit)
    Expected result: both groups are balanced within the allowable range (to the lower limit).
    '''
    students = __initialize_students(8)

    configuration["target_group_size"] = 5
    configuration["target_minus_one_allowed"] = True
    configuration["target_plus_one_allowed"] = False
    group_count: int = 2

    group_1: models.GroupRecord = models.GroupRecord("1", students[0:3])
    group_2: models.GroupRecord = models.GroupRecord("2", students[3:8])

    grouper2 = grouper_2.Grouper2(
        students, configuration, 2, printer.GroupingConsolePrinter())
    grouper2.groups = [group_1, group_2]
    assert len(group_1.members) == 3
    assert len(group_2.members) == 5

    grouper2.balance_groups()
    out, err = capfd.readouterr()

    assert ('balancing group: 1 with size 3') in out
    assert len(group_1.members) == 4
    assert len(group_2.members) == 4


def test_balance_groups_start_unbalanced_3(capfd):
    '''
    This test verifies the balance_groups and balance_group functions for the situation where:
        - groups smaller than target group size are NOT allowed
        - groups larger than target group size are allowed
        - group 1 one below the target (less than the lower limit)
        - group 2 one student higher than allowable limit
    Expected result: both groups are balanced within the allowable range.
    '''
    students = __initialize_students(7)

    configuration["target_group_size"] = 3
    configuration["target_minus_one_allowed"] = False
    configuration["target_plus_one_allowed"] = True
    group_count: int = 2

    group_1: models.GroupRecord = models.GroupRecord("1", students[0:5])
    group_2: models.GroupRecord = models.GroupRecord("2", students[5:7])

    grouper2 = grouper_2.Grouper2(
        students, configuration, 2, printer.GroupingConsolePrinter())
    grouper2.groups = [group_1, group_2]
    assert len(group_1.members) == 5
    assert len(group_2.members) == 2

    grouper2.balance_groups()
    out, err = capfd.readouterr()

    assert ('balancing group: 2 with size 2') in out
    assert len(group_1.members) == 4
    assert len(group_2.members) == 3


def test_balance_groups_start_unbalanced_4(capfd):
    '''
    This test verifies the balance_groups and balance_group functions for the situation where:
        - groups smaller than target group size are allowed
        - groups larger than target group size are allowed
        - group 1 one below the lower limit
        - group 2 one above the upper limit
    Expected result: both groups are balanced within the allowable range.
    '''
    students = __initialize_students(12)

    configuration["target_group_size"] = 6
    configuration["target_minus_one_allowed"] = True
    configuration["target_plus_one_allowed"] = True
    group_count: int = 2

    group_1: models.GroupRecord = models.GroupRecord("1", students[0:4])
    group_2: models.GroupRecord = models.GroupRecord("2", students[4:12])

    grouper2 = grouper_2.Grouper2(
        students, configuration, 2, printer.GroupingConsolePrinter())
    grouper2.groups = [group_1, group_2]
    assert len(group_1.members) == 4
    assert len(group_2.members) == 8

    grouper2.balance_groups()
    out, err = capfd.readouterr()

    assert ('balancing group: 1 with size 4') in out
    assert len(group_1.members) == 5
    assert len(group_2.members) == 7


def test_add_student_to_group_too_many_students(capfd):
    '''
    This test verifies that the add_student_to_group function will output a 
        message indicating that it isn't possible to group a student if all
        of the groups are already full (rather than making a group too large).
    '''
    students = __initialize_students(11)

    configuration["target_group_size"] = 5
    configuration["target_minus_one_allowed"] = False
    configuration["target_plus_one_allowed"] = False
    group_count: int = 2

    group_1: models.GroupRecord = models.GroupRecord("1", [])
    group_2: models.GroupRecord = models.GroupRecord("2", [])

    grouper2 = grouper_2.Grouper2(
        students, configuration, 2, printer.GroupingConsolePrinter())
    grouper2.groups = [group_1, group_2]
    assert len(group_1.members) == 0
    assert len(group_2.members) == 0

    for student in students:
        grouper2.add_student_to_group(student)

    out, err = capfd.readouterr()

    assert ('unable to group student with id: 11') in out
    assert len(group_1.members) == 5
    assert len(group_2.members) == 5
