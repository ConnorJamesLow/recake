from commands.util.manager import Manager
import click
from commands.util import util

@click.command('open')
@click.argument('identifier')
@click.option(
    '--no-cache',
    is_flag=True,
    help='Opens to a source.')
def command(identifier: str = '', no_cache: bool = False):
    """
    Open a source.
    """
    Manager().open(identifier, no_cache)
    util.fin('Launching')
