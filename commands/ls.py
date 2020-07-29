import click
from commands.util.source import Source
from commands.util.manager import Manager


@click.command('ls')
@click.argument('attrs', nargs=-1)
@click.option(
    '--truncate',
    is_flag=True,
    help='Shortened source names')
def command(truncate: bool, attrs):
    """
    List all sources.
    """
    if not attrs:
        click.echo(Manager().ls(truncate, 'id', 'name', 'source'))
        return

    if  '*' in attrs:
        click.echo(Manager().ls(truncate, 'id', 'name', 'source', 'remake', 'type'))
        return
    click.echo(Manager().ls(truncate, *attrs))
    # click.echo(remakes.ls(truncate))
