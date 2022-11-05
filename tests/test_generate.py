import pytest
from app.data import generate


def test_generate_random_user_records():
    '''
    tests generating a random set of records
    '''
    record_count = 6
    records = generate.generate_random_user_records(record_count)
    assert len(records) == record_count
    for i, r in enumerate(records):
        assert records[i].disliked_students.count(records[i]) == 0

    for i, r in enumerate(records):
        assert records[i].preferred_students.count(records[i]) == 0


def test_generate_random_user_records_bad_count():
    '''
    tests that pass in a bad count
    '''
    with pytest.raises(Exception):
        generate.generate_random_user_records(0)


def test_format_records_as_table():
    '''
    tests formatting a list of userrecords as a table
    '''

    records = [generate.UserRecord("zach", ['charlie', 'carl'], ['john'],
                                   {
                                    1: ["tuesday"], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []
                                   })]
    table = generate.format_records_as_table(records)
    assert table[0][0] == 'zach' # asurite set correctly
    assert table[0][1] == 'tuesday' # availability mapped correctly
    assert table[0][2] == '' # empty availability set correct
    assert table[0][9] == 'charlie' # preferred person set correct
    assert table[0][10] == 'carl'

    assert table[0][14] == 'john' # disliked person set correctly


def test_get_random_availability():
    '''
    tests generating a dict for random availability
    '''
    avail = generate.get_random_availability(timeslice=12)
    
    # 12 hr timeslice means there are 2 availability slots
    assert len(avail.keys()) == 2

def test_get_random_availability_raises_exception():
    '''
    tests get_random_availability and raises an exception from input
    '''

    with pytest.raises(Exception):
        generate.get_random_availability(timeslice=23)
