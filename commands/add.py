import click
from commands.util.source import Source


@click.group('add')
def command():
    """
    Commands for adding sources/etc.
    """
    pass


@command.command('source')
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
def source(source: str, name: str = '', source_type: str = 'local'):
    """
    The entry function for the source command
    """
    s = Source(src = source, name = name, _type = source_type)
    s.save()
