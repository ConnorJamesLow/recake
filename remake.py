# cli.py
import click
from commands import add, use, clip, copy


@click.group()
def cli():
    pass

cli.add_command(add.command)
# cli.add_command(use.command)
cli.add_command(clip.command)
cli.add_command(copy.command)

if __name__ == "__main__":
    cli()
