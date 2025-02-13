# # --- Copyright (c) 2024-2025 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""Module cli: Command Line Interface for the gitlab_monitor application.

:raises typer.Exit: mean that nothing else needs to be executed after this.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

import typer

from gitlab_monitor import __app_name__
from gitlab_monitor import __version__
from gitlab_monitor.commands.commands import CLICommand
from gitlab_monitor.logger import logger


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


def _verbose_callback(verbose) -> None:
    """Handle the verbose option.

    :param verbose: True if the verbose option is set.
    :type verbose: bool
    """
    logger.set_verbose(verbose)


@app.command(name="scan-projects")
def scan_projects(
    no_db: bool = typer.Option(
        False,
        "--no-database",
        help="Retrieve project without saving or updating it in the database",
    ),
    unused_since: datetime = typer.Option(
        None,
        "--unused-since",
        help="Retrieve projects unused since the specified date (format: YYYY-MM-DD)",
    ),
    save_in_file: str = typer.Option(
        None,
        "--save-in-file",
        help="Would store the projects retrieved in a json file with the specified name, \
stored in the project's “saved_datas/projects” folder.",
    ),
):
    """Scan and retrieve all projects from GitLab"""
    cli_command = CLICommand()
    command = cli_command.create_command("scan_projects")
    cli_command.handle_command(
        command, no_db=no_db, unused_since=unused_since, save_in_file=save_in_file
    )


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
    save_in_file: str = typer.Option(
        None,
        "--save-in-file",
        help="Would store the project retrieved in a json file with the specified name, \
stored in the project's “saved_datas/projects” folder.",
    ),
):
    """Scan and retrieve a GitLab project by its ID"""
    cli_command = CLICommand()
    command = cli_command.create_command("scan_project")
    cli_command.handle_command(
        command,
        id=project_id,
        get_commits=commit,
        no_db=no_db,
        save_in_file=save_in_file,
    )


def validate_project(project: str):
    """Valid if the project is a valid ID or path."""
    if project.isdigit():
        return int(project)
    if Path(project).exists():
        return Path(project)
    raise typer.BadParameter(
        "The argument must be a valid ID (integer) or a valid JSON file (path)."
    )


@app.command(name="archive-project")
def archive_project(
    project: str = typer.Argument(
        ...,
        help="Id of the project to archive or the path to a json file containing \
the projects to archive",
    ),
):
    """Archive a GitLab project by its ID or archive all the project \
        saved in the file passed as argument"""
    try:
        is_valid_project = validate_project(project)
        if isinstance(is_valid_project, int):
            typer.echo(f"Given ID : {is_valid_project}")
        elif isinstance(is_valid_project, Path):
            typer.echo(f"Given Path : {is_valid_project}")

        cli_command = CLICommand()
        command = cli_command.create_command("archive_project")
        cli_command.handle_command(command, project=project)

    except typer.BadParameter as e:
        typer.echo(f"Error : {e}", err=True)
        raise typer.Exit(code=1)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=_version_callback,
        help="Show the application's version and exit.",
        is_eager=True,
    ),
    verbose: Optional[bool] = typer.Option(
        None,
        "--verbose",
        "-vb",
        callback=_verbose_callback,
        help="Enable verbose mode for detailed logging.",
    ),
) -> None:
    """Main entry point for the CLI application."""
    if version:
        _version_callback(version)
    if verbose:
        _verbose_callback(verbose)
