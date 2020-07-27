import click
from commands.util.source import Source


@click.command('copy')
@click.argument('id')
@click.argument('destination')
@click.option(
    '--no-cache',
    is_flag=True,
    help='Copy directly from the source instead of the saved remake.')
def command(id: str = '', destination: str = '', no_cache: bool = False):
    """
    Copy a source to a destination.
    """
    Source(name=id, id=id).remake(destination, no_cache)
