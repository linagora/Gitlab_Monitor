# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from typing import Optional

import typer

from gitlab_monitor import __app_name__
from gitlab_monitor import __version__
from gitlab_monitor.commands.commands import CLICommand


app = typer.Typer()


@app.command(name="scan-projects")
def scan_projects():
    """Scan et récupère tous les projets du gitlab"""
    cli_command = CLICommand()
    command = cli_command.create_command("scan_projects")
    cli_command.handle_command(command)


@app.command(name="scan-project")
def scan_project(id: int):
    """Scan et récupère un projet gitlab depuis son id"""
    cli_command = CLICommand()
    command = cli_command.create_command("scan_project")
    cli_command.handle_command(command, id=id)


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
