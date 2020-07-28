import click
from commands.util.source import Source
from commands.util.manager import Manager


@click.command('list')
@click.option(
    '--truncate',
    is_flag=True,
    help='Shortened source names')
def command(truncate: bool):
    """
    List all sources.
    """
    remakes = Manager()
    click.echo(remakes.list(truncate))
