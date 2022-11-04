from app import models, validate


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

    group = [models.SurveyRecord(
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
    )]

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

    group = [models.SurveyRecord(
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
    )]

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

    group = [models.SurveyRecord(
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
    )]

    assert validate.fits_group_availability(user, group, 2)


def test_group_availability():
    group = [models.SurveyRecord(
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
    )]

    availability = validate.group_availability(group)

    assert availability['1']['monday'] == False
    assert availability['2']['tuesday'] == False
    assert availability['7']['friday'] == True


def test_availability_overlap_count():
    group = [models.SurveyRecord(
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
    )]

    avail_count = validate.availability_overlap_count(group)

    assert avail_count == 3


def test_meets_availability_requirement():
    group = [models.SurveyRecord(
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
    )]

    assert validate.meets_group_availability_requirement(group, 3)


def test_group_dislike_occurrences():
    group = [models.SurveyRecord(
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
    )]

    occurrences = validate.group_dislike_occurrences(group)

    assert occurrences['asurite1'] == ['asurite2']
    assert occurrences['asurite2'] == []
    assert occurrences['asurite5'] == []


def test_group_dislikes_user():
    user = 'asurite2'
    group = [models.SurveyRecord(
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
    )]

    group_dislikes = validate.group_dislikes_user(user, group)

    assert group_dislikes['asurite1'] == True
    assert group_dislikes['asurite3'] == True
    assert group_dislikes['asurite4'] == False


def test_user_dislikes_group():
    user = models.SurveyRecord(
        student_id="asurite1",
        disliked_students=['asurite2', 'asurite3', 'asurite17']
    )
    group = [models.SurveyRecord(
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
    )]

    group_dislikes = validate.user_dislikes_group(user, group)

    assert len(group_dislikes) == 2


def test_meets_group_dislike_requirement():
    user = models.SurveyRecord(
        student_id="asurite1",
        disliked_students=['asurite2', 'asurite3', 'asurite17']
    )
    group = [models.SurveyRecord(
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
    )]

    assert not (validate.meets_group_dislike_requirement(user, group, 1))
    assert validate.meets_group_dislike_requirement(user, group, 2)
