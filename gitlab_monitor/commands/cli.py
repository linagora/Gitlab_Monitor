from typing import Optional

import typer
from commands.commands import CLICommand
from gitlab_monitor import __app_name__, __version__

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command(name="scan_projets")
def scan_projects():
    """Scan et récupère tous les projets du gitlab"""
    cli_command = CLICommand()
    command = cli_command.create_command("scan_projects")
    cli_command.handle_command(command)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Montre la  version de l'application et quitte le programme",
        is_eager=True,
    )
) -> None:
    return
