import click

@click.command()
@click.option('--name', default='nobody', help='your name.')

def hello(name) :
    click.echo(f"Hello, {name}.")

if __name__ == '__main__':
    hello()