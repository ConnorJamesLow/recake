import click
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

    if '*' in attrs:
        m = Manager()
        click.echo(
            m.ls(truncate, 'id', 'name', 'source', 'recake', 'type'))
        return
    click.echo(Manager().ls(truncate, *attrs))
    # click.echo(recakes.ls(truncate))
