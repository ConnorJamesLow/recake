import click
from commands.util import util
from commands.util.manager import Manager

@click.command('rm')
@click.argument('name')
@click.option(
    '--keep',
    is_flag=True,
    help='Do not remove the record: just clear the cache.')
def command(name: str = '', keep: bool = False):
    """
    Delete an existing source.
    """
    if keep:
        click.echo('--keep: will not remove the source from the list, only the cached content.')
    m = Manager()
    m.clear(name, not keep)
    util.fin(f'Successfully removed {name}.')
