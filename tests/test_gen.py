'''Test for the gen command'''
from click.testing import CliRunner
from app.commands import gen


def test_gen(mocker):
  '''
  Still a wip. Haven't quite figured out how to unit test cli commands and use the mock framework
  '''
  runner = CliRunner()
  mocker.patch('app.generate.generate_random_user_records')
  mocker.patch('app.generate.format_records_as_table')
  mocker.patch('app.file.output.output_to_csv')
  res = runner.invoke(gen.gen, ['--filename', 'test.csv', '--count', '10'])
  assert res.exit_code == 0
