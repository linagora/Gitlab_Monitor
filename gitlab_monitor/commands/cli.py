# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""Module cli: Command Line Interface for the gitlab_monitor application.

:raises typer.Exit: mean that nothing else needs to be executed after this.
"""

from typing import Annotated
from typing import Optional

import typer

from gitlab_monitor import __app_name__
from gitlab_monitor import __version__
from gitlab_monitor.commands.commands import CLICommand


app = typer.Typer()


def _version_callback(value: bool) -> None:
    """Handle the version option.

    :param value: True if the version option is set.
    :type value: bool
    :raises typer.Exit: mean that nothing else needs to be executed after this.
    """
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command(name="scan-projects")
def scan_projects(
    no_db: bool = typer.Option(
        False,
        "--no-database",
        help="Retrieve project without saving or updating it in the database",
    ),
):
    """Scan and retrieve all projects from GitLab"""
    cli_command = CLICommand()
    command = cli_command.create_command("scan_projects")
    cli_command.handle_command(command, no_db=no_db)


@app.command(name="scan-project")
def scan_project(
    project_id: int = typer.Argument(..., help="The ID of the project to scan"),
    commit: bool = typer.Option(
        False, "-c", "--commit", help="Include commit in the scan"
    ),
    no_db: bool = typer.Option(
        False,
        "--no-database",
        help="Retrieve project without saving or updating it in the database",
    ),
):
    """Scan and retrieve a GitLab project by its ID"""
    cli_command = CLICommand()
    command = cli_command.create_command("scan_project")
    cli_command.handle_command(command, id=project_id, get_commits=commit, no_db=no_db)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=_version_callback,
        help="Show the application's version and exit.",
        is_eager=True,
    )
) -> None:
    """Main entry point for the CLI application."""
    if version:
        _version_callback(version)
