'''
gen contains all of the commands in the gen subgroup
'''
import click
from app import generate
from app.file import output

@click.group("gen")
def gen():
    '''
    commands for generating datasets
    '''

@gen.command("dataset")
@click.option('--filename', default="dataset.csv")
@click.option('--count', default=20)
def dataset(filename: str, count: int):
    '''
    dataset generates a new sample dataset containing
    the necessary criteria to use for running the algorithm
    '''
    user_records = generate.generate_random_user_records(count)
    body = generate.format_records_as_table(user_records)
    headers = [
        'asurite', '0 to 3 AM', '3 to 6 AM', '6 to 9 AM', '9 to 12 PM',
        '12 to 3 PM', '3 to 6 PM', '6 to 9 PM', '9 to 12 AM', 'preferred 1',
        'preferred 2', 'preferred 3', 'preferred 4', 'preferred 5',
        'disliked 1', 'disliked 2', 'disliked 3'
    ]
    output.output_to_csv(headers, body, filename)