'''
gen contains all of the commands in the gen subgroup
'''
import click
from app import generate
from app.file import output
from app.algorithm import ga, models


@click.command("gen")
@click.option('--filename', default="dataset.csv")
@click.option('--count', default=20)
def gen(filename: str, count: int):
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

    groups = ga.grouping_algorithm(user_records, 4)
    for g in groups:
        print()
        print(f"meets availability: {g.meets_availability_requirement()}")
        print(f"meets dislike requirement: {models.meets_dislike_requirement(g.members)}")
        for u in g.members:
            print(u.asurite)
    output.output_to_csv(headers, body, filename)
