import click
from commands.util.manager import Manager

@click.command('add')
@click.argument('source')
@click.option(
    '-n',
    '--name',
    help='A name to use when referencing the source later.')
@click.option(
    '-t',
    '--source-type',
    help='The source type.',
    type=click.Choice(['local', 'web']),
    default='local')
def command(source: str, name: str = '', source_type: str = 'local'):
    """
    Add a new source.
    """
    m = Manager()
    m.add(source, name, source_type)
