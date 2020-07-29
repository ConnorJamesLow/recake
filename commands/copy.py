from commands.util.manager import Manager
import click


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
    Manager().copy(destination, id, no_cache)
