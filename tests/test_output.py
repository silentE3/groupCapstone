import csv
import os
import app.file.output

def test_output_to_csv():
    filepath = 'tests/testout.csv'
    headers = ['hi', 'my', 'name', 'is', 'zach' ]
    body = [['a', 'b', 'c', 'd', 'e'], ['a', 'b', 'c', 'd', 'e'],
            ['a', 'b', 'c', 'd', 'e']]

    app.file.output.output_to_csv(headers, body, filepath)

    with open(filepath, 'r') as file:
      r = csv.reader(file)

      assert next(r) == headers
      
    res = os.stat(filepath)
    os.remove(filepath)