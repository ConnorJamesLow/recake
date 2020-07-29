# cli.py
import click
from commands import add, ls, clip, copy, open

@click.version_option('0.1.0', prog_name='remake', message='%(prog)s v%(version)s')
@click.group()
def cli():
    pass

cli.add_command(add.command)
# cli.add_command(use.command)
cli.add_command(clip.command)
cli.add_command(copy.command)
cli.add_command(ls.command)
cli.add_command(open.command)

if __name__ == "__main__":
    cli()
