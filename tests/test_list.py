'''
This file contains test methods for the list file.
'''
from app.data import list
from app import models

def test_list_1():
    result = []

    ids = []
    ids.append("asurite1")
    ids.append("asurite2")
    ids.append("asurite3")
    ids.append("asurite4")
    ids.append("asurite5")
    ids.append("asurite6")

    survey = []

    result = list.StudentList.add_students(self, survey, ids)