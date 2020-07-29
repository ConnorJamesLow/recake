from commands.util.manager import Manager
import click


@click.command('clip')
@click.argument('id')
@click.option(
    '--no-cache',
    is_flag=True,
    help='Copy directly from the source instead of the saved recake.')
def command(id: str = '', no_cache: bool = False):
    """
    Copy a single-file source to the clipboard. ID can be either the name or the generated id of the source.
    """
    # Source(name=id, id=id).clip(no_cache)
    Manager().clip(id, no_cache)
    click.echo(click.style('Copied!', fg='green'))
