import click
from commands.util.manager import Manager

@click.command('update')
@click.argument('name')
def command(name: str = ''):
    """
    Update the cached content with the source.  
    Reference by name or id.
    """
    m = Manager()
    m.update(name)
