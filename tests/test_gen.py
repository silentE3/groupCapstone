'''Test for the gen command'''
from click.testing import CliRunner
from app.commands import generate
from app import output


def test_gen(mocker):
    '''
    Still a wip. Haven't quite figured out how to unit test cli commands and use the mock framework
    '''
    runner = CliRunner()
    mocker.patch('app.data.generate.generate_random_user_records')
    mocker.patch('app.data.generate.format_records_as_table')
    mocker.patch.object(output.SurveyDataWriter, 'output_to_csv', return_value=None)
    res = runner.invoke(
        generate.gen, ['--filename', 'test.csv', '--count', '10'])
    assert res.exit_code == 0
