'''
Output tests
'''
import csv
import os
from app import output, models

def test_output_to_csv():
    '''
    Test the output WriteSurveyData
    '''
    filepath = 'tests/testout.csv'
    headers = ['hi', 'my', 'name', 'is', 'zach' ]
    body = [['a', 'b', 'c', 'd', 'e'], ['a', 'b', 'c', 'd', 'e'],
            ['a', 'b', 'c', 'd', 'e']]

    writer = output.WriteSurveyData()
    writer.output_to_csv(headers, body, filepath)

    with open(filepath, 'r',  encoding="UTF-8") as file:
        reader = csv.reader(file)
        assert next(reader) == headers

    os.stat(filepath)
    os.remove(filepath)
    
def test_group_output_to_csv():
    '''
    Test the creating of a CSV file from grouping data
    '''

    survey1 = models.SurveyRecord("a1", "Bobby Boucher", "bboucher@asu.edu", "bobouch", "UTC-7" )
    survey2 = models.SurveyRecord("a2", "Spongebob Squarepants", "sspuare@asu.edu", "sposqu", "UTC-7" )
    survey3 = models.SurveyRecord("a3", "Homelander", "hlander@asu.edu", "hland", "UTC-7" )
    survey4 = models.SurveyRecord("a4", "Some Guy", "sguy@asu.edu", "someguy", "UTC-7" )
    group1 = models.GroupRecord("Group #1", [survey1, survey2])
    group2 = models.GroupRecord("Group #2", [survey3, survey4])

    groups = [group1, group2]
    mapping:models.SurveyFieldMapping = {
        "student_id_field_name":"", 
        "student_name_field_name":"", 
        "student_email_field_name":"", 
        "student_login_field_name":"", 
        "timezone_field_name":"", 
        "preferred_students_field_names":[], 
        "disliked_students_field_names":[], 
        "availability_field_names":[]}
    config:models.Configuration = {
        "class_name":"ser486",
        "target_group_size":2,
        "grouping_passes":2,
        "field_mappings":mapping,
        "output_student_name":True,
        "output_student_email":True,
        "output_student_login":True}

    filename = "test_group_csv_output.csv"
    writer = output.WriteGroupingData(config)
    writer.output_groups_csv(groups, filename)

    expected = "group id,student id,student name,student email,student login\ngroup_1,a1,Bobby Boucher,bboucher@asu.edu,bobouch\ngroup_1,a2,Spongebob Squarepants,sspuare@asu.edu,sposqu\ngroup_2,a3,Homelander,hlander@asu.edu,hland\ngroup_2,a4,Some Guy,sguy@asu.edu,someguy\n"

    results = ''
    with open(filename, 'r', encoding="UTF-8") as file:                
        for line in file:
            results += line
         

    assert results == expected

