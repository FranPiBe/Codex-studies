"""A tiny CLI wrapper around a few git commands using Click."""

import subprocess
import click


@click.group()
def cli():
    """Wrapper around common git commands"""


def run_git_command(args):
    subprocess.run(["git"] + list(args), check=False)


@cli.command()
@click.argument("path", default=".")
def status(path):
    """Show git status"""
    run_git_command(["-C", path, "status"])


@cli.command()
@click.argument("message")
def commit(message):
    """Commit staged changes with a message"""
    run_git_command(["commit", "-m", message])


if __name__ == "__main__":
    cli()
