from commands.util.manager import Manager
import click
from commands.util import util

@click.command('open')
@click.argument('identifier')
@click.option(
    '--cached',
    is_flag=True,
    help='Open to the cached code instead of the source.')
def command(identifier: str = '', cached: bool = False):
    """
    Open a source.
    """
    Manager().open(identifier, cached)
    util.fin('Launching')
