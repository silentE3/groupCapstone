from app import models
from app.group import validate


def test_user_availability():
    user = models.SurveyRecord(
        student_id="asurite1",
        availability={
            "1": ['monday', 'tuesday', 'wednesday'],
            "2": ['wednesday'],
            "3": ['monday'],
            "4": ['monday'],
            "5": ['sunday'],
            "6": ['thursday'],
            "7": ['friday']
        },
    )

    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite2",
        availability={
            "1": ['monday', ],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    ), models.SurveyRecord(
        student_id="asurite3",
        availability={
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    )])

    availability = validate.user_availability(user, group)

    assert availability["1"]["monday"] == False
    assert availability["6"]["thursday"] == True


def test_user_matches_availability_count():
    user = models.SurveyRecord(
        student_id="asurite1",
        availability={
            "1": ['monday', 'tuesday', 'wednesday'],
            "2": ['wednesday'],
            "3": ['monday'],
            "4": ['monday'],
            "5": ['sunday'],
            "6": ['thursday'],
            "7": ['friday']
        },
    )

    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite2",
        availability={
            "1": ['monday', ],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    ), models.SurveyRecord(
        student_id="asurite3",
        availability={
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    )])

    match_count = validate.user_matches_availability_count(user, group)

    assert match_count == 2


def test_fits_group_availability():
    user = models.SurveyRecord(
        student_id="asurite1",
        availability={
            "1": ['monday', 'tuesday', 'wednesday'],
            "2": ['wednesday'],
            "3": ['monday'],
            "4": ['monday'],
            "5": ['sunday'],
            "6": ['thursday'],
            "7": ['friday']
        },
    )

    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite2",
        availability={
            "1": ['monday', ],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    ), models.SurveyRecord(
        student_id="asurite3",
        availability={
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    )])

    assert validate.fits_group_availability(user, group, 2)


def test_group_availability():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        availability={
            "1": ['monday'],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    ), models.SurveyRecord(
        student_id="asurite3",
        availability={
            "1": [],
            "2": ['tuesday'],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    ), models.SurveyRecord(
        student_id="asurite4",
        availability={
            "1": ['monday'],
            "2": ['tuesday'],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    )])

    availability = validate.group_availability(group)

    assert availability['1']['monday'] == False
    assert availability['2']['tuesday'] == False
    assert availability['7']['friday'] == True


def test_group_availability_strings_1():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        availability={
            "1": ['tuesday', 'wednesday'],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    ), models.SurveyRecord(
        student_id="asurite3",
        availability={
            "1": ['monday', 'tuesday', 'wednesday'],
            "2": ['tuesday'],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": []
        },
    ), models.SurveyRecord(
        student_id="asurite4",
        availability={
            "1": ['tuesday', 'wednesday', 'friday'],
            "2": ['tuesday'],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    )])

    availability = validate.group_availability_strings(group)

    assert "monday @ 1" not in availability
    assert "tuesday @ 1" in availability
    assert "wednesday @ 1" in availability
    assert "thursday @ 1" not in availability
    assert "friday @ 1" not in availability
    assert "saturday @ 1" not in availability
    assert "sunday @ 1" not in availability

    # Note: only checked EVERY day above for robustness. Not necessary throughout
    assert sum(map(lambda x: '@ 2' in x, availability)) == 0
    assert sum(map(lambda x: '@ 3' in x, availability)) == 0
    assert sum(map(lambda x: '@ 4' in x, availability)) == 0
    assert sum(map(lambda x: '@ 5' in x, availability)) == 0

    assert "thursday @ 6" in availability
    assert sum(map(lambda x: '@ 6' in x, availability)) == 1

    assert sum(map(lambda x: '@ 7' in x, availability)) == 0


def test_group_availability_strings_2():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        availability={
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]": ['tuesday', 'wednesday'],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]": [],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]": [],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]": [],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]": [],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]": ['thursday'],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]": ['friday']
        },
    ), models.SurveyRecord(
        student_id="asurite3",
        availability={
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]": ['monday', 'tuesday', 'wednesday'],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]": ['tuesday'],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]": [],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]": [],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]": [],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]": ['thursday'],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]": []
        },
    ), models.SurveyRecord(
        student_id="asurite4",
        availability={
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]": ['tuesday', 'wednesday', 'friday'],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]": ['tuesday'],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]": [],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]": [],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]": [],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]": ['thursday'],
            "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]": ['friday']
        },
    )])

    availability = validate.group_availability_strings(group)

    assert "monday @ 0:00 AM - 3:00 AM" not in availability
    assert "tuesday @ 0:00 AM - 3:00 AM" in availability
    assert "wednesday @ 0:00 AM - 3:00 AM" in availability
    assert "thursday @ 0:00 AM - 3:00 AM" not in availability
    assert "friday @ 0:00 AM - 3:00 AM" not in availability
    assert "saturday @ 0:00 AM - 3:00 AM" not in availability
    assert "sunday @ 0:00 AM - 3:00 AM" not in availability

    # Note: only checked EVERY day above for robustness. Not necessary throughout
    assert sum(map(lambda x: '@ 3:00 AM - 6:00 AM' in x, availability)) == 0
    assert sum(map(lambda x: '@ 6:00 AM - 9:00 AM' in x, availability)) == 0
    assert sum(map(lambda x: '@ 9:00 AM - 12:00 PM' in x, availability)) == 0
    assert sum(map(lambda x: '@ 12:00 PM - 3:00 PM' in x, availability)) == 0

    assert "thursday @ 3:00 PM - 6:00 PM" in availability
    # verify '@ 6'is only in the list once
    assert sum(map(lambda x: '@ 3:00 PM - 6:00 PM' in x, availability)) == 1

    assert sum(map(lambda x: '@ 6:00 PM - 9:00 PM' in x, availability)) == 0


def test_availability_overlap_count():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        availability={
            "1": ['monday'],
            "2": ['tuesday'],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    ), models.SurveyRecord(
        student_id="asurite3",
        availability={
            "1": [],
            "2": ['tuesday'],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    ), models.SurveyRecord(
        student_id="asurite4",
        availability={
            "1": ['monday'],
            "2": ['tuesday'],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    )])

    avail_count = validate.availability_overlap_count(group)

    assert avail_count == 3


def test_meets_availability_requirement():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        availability={
            "1": ['monday'],
            "2": ['tuesday'],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    ), models.SurveyRecord(
        student_id="asurite3",
        availability={
            "1": [],
            "2": ['tuesday'],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    ), models.SurveyRecord(
        student_id="asurite4",
        availability={
            "1": ['monday'],
            "2": ['tuesday'],
            "3": [],
            "4": [],
            "5": [],
            "6": ['thursday'],
            "7": ['friday']
        },
    )])

    assert validate.meets_group_availability_requirement(group, 3)


def test_do_duplicate_users_exist():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
    )])

    assert not validate.duplicate_user_in_group(group)


def test_do_duplicate_users_exist_2():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite2",
    )])

    assert validate.duplicate_user_in_group(group)


def test_do_duplicate_users_exist_in_groups():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
    )])
    group2 = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite6",
    ), models.SurveyRecord(
        student_id="asurite7",
    ), models.SurveyRecord(
        student_id="asurite8",
    ), models.SurveyRecord(
        student_id="asurite9",
    ), models.SurveyRecord(
        student_id="asurite10",
    )])

    groups = [group, group2]

    assert not validate.duplicate_user_in_dataset(groups)


def test_do_duplicate_users_exist_in_groups_2():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
    )])
    group2 = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite6",
    ), models.SurveyRecord(
        student_id="asurite7",
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite9",
    ), models.SurveyRecord(
        student_id="asurite10",
    )])
    groups = [group, group2]
    assert validate.duplicate_user_in_dataset(groups)


def test_do_duplicate_users_exist_in_groups_3():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
    ), models.SurveyRecord(
        student_id="asurite4",
    )])
    group2 = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite6",
    ), models.SurveyRecord(
        student_id="asurite5",
    )])
    group3 = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite9",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite7",
    ), models.SurveyRecord(
        student_id="asurite8",
    )])
    groups = [group, group2, group3]
    assert validate.duplicate_user_in_dataset(groups)


def test_group_dislike_occurrences():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        disliked_students=['asurite2']
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
        disliked_students=['asurite5', 'asurite6']
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
        disliked_students=['asurite10']
    ), models.SurveyRecord(
        student_id="asurite6",
    )])

    occurrences = validate.group_dislike_occurrences(group)

    assert occurrences['asurite1'] == ['asurite2']
    assert occurrences['asurite2'] == []
    assert occurrences['asurite5'] == []


def test_group_dislikes_user():
    user = 'asurite2'
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        disliked_students=['asurite2']
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
        disliked_students=['asurite2', 'asurite6']
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
        disliked_students=['asurite2']
    ), models.SurveyRecord(
        student_id="asurite6",
    )])

    group_dislikes = validate.group_dislikes_user(user, group)

    assert group_dislikes['asurite1'] == True
    assert group_dislikes['asurite3'] == True
    assert group_dislikes['asurite4'] == False


def test_user_dislikes_group():
    user = models.SurveyRecord(
        student_id="asurite1",
        disliked_students=['asurite2', 'asurite3', 'asurite17']
    )
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
        disliked_students=['asurite2', 'asurite6']
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
        disliked_students=['asurite2']
    ), models.SurveyRecord(
        student_id="asurite6",
    )])

    group_dislikes = validate.user_dislikes_group(user, group)

    assert len(group_dislikes) == 2


def test_meets_group_dislike_requirement():
    user = models.SurveyRecord(
        student_id="asurite1",
        disliked_students=['asurite2', 'asurite3', 'asurite17']
    )
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
        disliked_students=['asurite2', 'asurite6']
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
        disliked_students=['asurite2']
    ), models.SurveyRecord(
        student_id="asurite6",
    )])

    assert not (validate.meets_group_dislike_requirement(user, group, 1))
    assert validate.meets_group_dislike_requirement(user, group, 2)


def test_group_like_occurrences():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        preferred_students=['asurite2']
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
        preferred_students=['asurite5', 'asurite6']
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
        preferred_students=['asurite10']
    ), models.SurveyRecord(
        student_id="asurite6",
    )])

    occurrences = validate.group_like_occurrences(group)

    assert occurrences['asurite1'] == ['asurite2']
    assert occurrences['asurite2'] == []
    assert occurrences['asurite5'] == []


def test_meets_like_requirements():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        preferred_students=['asurite2']
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
        preferred_students=['asurite5', 'asurite6']
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
        preferred_students=['asurite10']
    ), models.SurveyRecord(
        student_id="asurite6",
    )])

    assert validate.meets_like_requirement(group, 3)
    assert not validate.meets_like_requirement(group, 5)
    assert validate.meets_like_requirement(group, 0)


def test_group_likes_user():
    user = 'asurite2'
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        preferred_students=['asurite2']
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
        preferred_students=['asurite2', 'asurite6']
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
        preferred_students=['asurite2']
    ), models.SurveyRecord(
        student_id="asurite6",
    )])

    group_likes = validate.group_likes_user(user, group)

    assert group_likes['asurite1'] == True
    assert group_likes['asurite3'] == True
    assert group_likes['asurite4'] == False


def test_user_likes_group():
    user = models.SurveyRecord(
        student_id="asurite1",
        preferred_students=['asurite2', 'asurite3', 'asurite17']
    )
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
        preferred_students=['asurite2', 'asurite6']
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
        preferred_students=['asurite2']
    ), models.SurveyRecord(
        student_id="asurite6",
    )])

    group_likes = validate.user_likes_group(user, group)

    assert len(group_likes) == 2


def test_meets_group_like_requirement():
    user = models.SurveyRecord(
        student_id="asurite1",
        preferred_students=['asurite2', 'asurite3', 'asurite17']
    )
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
        preferred_students=['asurite2', 'asurite6']
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
        preferred_students=['asurite2']
    ), models.SurveyRecord(
        student_id="asurite6",
    )])

    assert (validate.meets_group_like_requirement(user, group, 1))
    assert not validate.meets_group_like_requirement(user, group, 3)


def test_size_limit():
    user1 = models.SurveyRecord(
        student_id="asurite1"
    )
    user2 = models.SurveyRecord(
        student_id="asurite2"
    )
    user3 = models.SurveyRecord(
        student_id="asurite3"
    )
    user4 = models.SurveyRecord(
        student_id="asurite4"
    )
    group1 = models.GroupRecord(
        group_id="group1",
        members=[user1, user2, user3, user4]
    )
    group_list = [group1]

    assert validate.size_limit_in_dataset(group_list, 4)


def test_size_limit_2():
    user1 = models.SurveyRecord(
        student_id="asurite1"
    )
    user2 = models.SurveyRecord(
        student_id="asurite2"
    )
    user3 = models.SurveyRecord(
        student_id="asurite3"
    )
    user4 = models.SurveyRecord(
        student_id="asurite4"
    )
    user5 = models.SurveyRecord(
        student_id="asurite5"
    )
    user6 = models.SurveyRecord(
        student_id="asurite6"
    )
    user7 = models.SurveyRecord(
        student_id="asurite7"
    )
    user8 = models.SurveyRecord(
        student_id="asurite8"
    )
    group1 = models.GroupRecord(
        group_id="group1",
        members=[user1, user2, user3, user4]
    )
    group2 = models.GroupRecord(
        group_id="group2",
        members=[user5, user6, user7, user8]
    )
    group_list = [group1, group2]

    assert validate.size_limit_in_dataset(group_list, 4)


def test_size_limit_3():
    user1 = models.SurveyRecord(
        student_id="asurite1"
    )
    user2 = models.SurveyRecord(
        student_id="asurite2"
    )
    user3 = models.SurveyRecord(
        student_id="asurite3"
    )
    user4 = models.SurveyRecord(
        student_id="asurite4"
    )
    user5 = models.SurveyRecord(
        student_id="asurite5"
    )
    user6 = models.SurveyRecord(
        student_id="asurite6"
    )
    user7 = models.SurveyRecord(
        student_id="asurite7"
    )
    group1 = models.GroupRecord(
        group_id="group1",
        members=[user1, user2, user3, user4]
    )
    group2 = models.GroupRecord(
        group_id="group2",
        members=[user5, user6]
    )
    group_list = [group1, group2]

    assert not validate.size_limit_in_dataset(group_list, 4)


def test_size_limit_4():
    user1 = models.SurveyRecord(
        student_id="asurite1"
    )
    user2 = models.SurveyRecord(
        student_id="asurite2"
    )
    user3 = models.SurveyRecord(
        student_id="asurite3"
    )
    user4 = models.SurveyRecord(
        student_id="asurite4"
    )
    user5 = models.SurveyRecord(
        student_id="asurite5"
    )
    user6 = models.SurveyRecord(
        student_id="asurite6"
    )
    user7 = models.SurveyRecord(
        student_id="asurite7"
    )
    user8 = models.SurveyRecord(
        student_id="asurite8"
    )
    user9 = models.SurveyRecord(
        student_id="asurite9"
    )
    group1 = models.GroupRecord(
        group_id="group1",
        members=[user1, user2, user3, user4, user5, user9]
    )
    group2 = models.GroupRecord(
        group_id="group2",
        members=[user6, user7, user8]
    )
    group_list = [group1, group2]

    assert not validate.size_limit_in_dataset(group_list, 4)


def test_total_disliked_pairings():
    group_1 = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        disliked_students=['asurite2']
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
        disliked_students=['asurite5', 'asurite6']
    )])  # 1 dislikes

    group_2 = models.GroupRecord("2", [models.SurveyRecord(
        student_id="asurite4",
        disliked_students=['asurite2']
    ), models.SurveyRecord(
        student_id="asurite5",
    ), models.SurveyRecord(
        student_id="asurite6",
        disliked_students=['asurite3', 'asurite7']
    )])  # 0 dislikes

    group_3 = models.GroupRecord("3", [models.SurveyRecord(
        student_id="asurite7",
        disliked_students=['asurite9']
    ), models.SurveyRecord(
        student_id="asurite8",
    ), models.SurveyRecord(
        student_id="asurite9",
        disliked_students=['asurite7', 'asurite8']
    )])  # 3 dislikes

    assert validate.total_disliked_pairings([group_1, group_2, group_3]) == 4


def test_total_groups_no_availability_1():
    group_1 = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        availability={
            "1": ['monday'],
            "2": [],
            "3": [],
        },
    ), models.SurveyRecord(
        student_id="asurite2",
        availability={
            "1": ['monday'],
            "2": [],
            "3": [],
        },
    ), models.SurveyRecord(
        student_id="asurite3",
        availability={
            "1": [],
            "2": [],
            "3": ['monday'],
        },
    )])  # NO overlapping slot

    group_2 = models.GroupRecord("2", [models.SurveyRecord(
        student_id="asurite4",
        availability={
            "1": ['monday'],
            "2": [],
            "3": [],
        },
    ), models.SurveyRecord(
        student_id="asurite5",
        availability={
            "1": ['monday'],
            "2": [],
            "3": [],
        },
    ), models.SurveyRecord(
        student_id="asurite6",
        availability={
            "1": ['monday', 'tuesday'],
            "2": [],
            "3": ['wednesday'],
        },
    )])  # overlapping slot

    group_3 = models.GroupRecord("3", [models.SurveyRecord(
        student_id="asurite7",
        availability={
            "1": [],
            "2": ['wednesday'],
            "3": [],
        },
    ), models.SurveyRecord(
        student_id="asurite8",
        availability={
            "1": [],
            "2": ['wednesday'],
            "3": [],
        },
    ), models.SurveyRecord(
        student_id="asurite9",
        availability={
            "1": [],
            "2": ['tuesday', 'wednesday'],
            "3": ['monday'],
        },
    )])  # overlapping slot

    assert validate.total_groups_no_availability(
        [group_1, group_2, group_3]) == 1  # 1 group WITHOUT an overlapping time slot


def test_total_groups_no_availability_2():
    group_1 = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        availability={
            "1": ['monday'],
            "2": [],
            "3": [],
        },
    ), models.SurveyRecord(
        student_id="asurite2",
        availability={
            "1": ['monday'],
            "2": [],
            "3": [],
        },
    ), models.SurveyRecord(
        student_id="asurite3",
        availability={
            "1": [],
            "2": [],
            "3": ['monday'],
        },
    )])  # No overlapping slot

    group_2 = models.GroupRecord("2", [models.SurveyRecord(
        student_id="asurite4",
        availability={
            "1": ['monday'],
            "2": [],
            "3": [],
        },
    ), models.SurveyRecord(
        student_id="asurite5",
        availability={
            "1": [],
            "2": ['monday'],
            "3": [],
        },
    ), models.SurveyRecord(
        student_id="asurite6",
        availability={
            "1": ['monday', 'tuesday'],
            "2": [],
            "3": ['wednesday'],
        },
    )])  # No overlapping slot

    group_3 = models.GroupRecord("3", [models.SurveyRecord(
        student_id="asurite7",
        availability={
            "1": [],
            "2": ['wednesday'],
            "3": [],
        },
    ), models.SurveyRecord(
        student_id="asurite8",
        availability={
            "1": [],
            "2": ['wednesday'],
            "3": [],
        },
    ), models.SurveyRecord(
        student_id="asurite9",
        availability={
            "1": [],
            "2": ['tuesday'],
            "3": ['monday'],
        },
    )])  # No overlapping slot

    assert validate.total_groups_no_availability(
        [group_1, group_2, group_3]) == 3  # 3 groups WITHOUT an overlapping time slot


def test_total_liked_pairings_1():
    group_1 = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        preferred_students=['asurite2']
    ), models.SurveyRecord(
        student_id="asurite2",
        preferred_students=['asurite1', 'asurite4']
    ), models.SurveyRecord(
        student_id="asurite3",
        preferred_students=['asurite6']
    )])  # 2 preferred pairings

    group_2 = models.GroupRecord("2", [models.SurveyRecord(
        student_id="asurite4",
        preferred_students=['asurite6']
    ), models.SurveyRecord(
        student_id="asurite5",
        preferred_students=['asurite1']
    ), models.SurveyRecord(
        student_id="asurite6",
        preferred_students=['asurite4', 'asurite5']
    )])  # 3 preferred pairings

    assert validate.total_liked_pairings([group_1, group_2]) == 5
