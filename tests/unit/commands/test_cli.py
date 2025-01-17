from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
import typer
from typer.testing import CliRunner

from gitlab_monitor.commands.cli import _verbose_callback
from gitlab_monitor.commands.cli import _version_callback
from gitlab_monitor.commands.cli import app
from gitlab_monitor.commands.cli import validate_project
from gitlab_monitor.logger import logger


runner = CliRunner()

# === Tests --version ===


def test_version_callback():
    with patch("typer.echo") as mock_echo:
        with pytest.raises(typer.Exit):
            _version_callback(True)
        mock_echo.assert_called_once_with("gitlab_monitor v1.0.0")


# === Tests scan-projects ===


@patch("gitlab_monitor.commands.cli.CLICommand")
def test_scan_projects(mock_cli_command):
    mock_command_instance = mock_cli_command.return_value
    mock_command_instance.create_command.return_value = MagicMock()

    result = runner.invoke(
        app, ["scan-projects", "--no-database", "--save-in-file", "test.json"]
    )

    assert result.exit_code == 0
    mock_cli_command.assert_called_once()
    mock_command_instance.create_command.assert_called_once_with("scan_projects")
    mock_command_instance.handle_command.assert_called_once_with(
        mock_command_instance.create_command.return_value,
        no_db=True,
        unused_since=None,
        save_in_file="test.json",
    )


# === Tests scan-project ===


@patch("gitlab_monitor.commands.cli.CLICommand")
def test_scan_project(mock_cli_command):
    mock_command_instance = mock_cli_command.return_value
    mock_command_instance.create_command.return_value = MagicMock()

    result = runner.invoke(
        app,
        [
            "scan-project",
            "123",
            "--commit",
            "--no-database",
            "--save-in-file",
            "project.json",
        ],
    )

    assert result.exit_code == 0
    mock_cli_command.assert_called_once()
    mock_command_instance.create_command.assert_called_once_with("scan_project")
    mock_command_instance.handle_command.assert_called_once_with(
        mock_command_instance.create_command.return_value,
        id=123,
        get_commits=True,
        no_db=True,
        save_in_file="project.json",
    )


def test_scan_project_missing_id():
    result = runner.invoke(app, ["scan-project"])
    assert result.exit_code != 0
    assert "Missing argument 'PROJECT_ID'" in result.output


# === Tests --verbose ===


def test_verbose_callback():
    with patch.object(logger, "set_verbose") as mock_set_verbose:
        _verbose_callback(True)
        mock_set_verbose.assert_called_once_with(True)


# === Tests validate_project ===


def test_validate_project_with_id():
    result = validate_project("123")
    assert result == 123


def test_validate_project_with_valid_path(tmp_path):
    valid_path = tmp_path / "projects.json"
    valid_path.write_text("[]")

    result = validate_project(str(valid_path))
    assert isinstance(result, Path)
    assert result.exists()


def test_validate_project_with_invalid_path():
    with pytest.raises(typer.BadParameter, match="The argument must be a valid ID.*"):
        validate_project("invalid_path")


def test_validate_project_with_invalid_id():
    with pytest.raises(typer.BadParameter, match="The argument must be a valid ID.*"):
        validate_project("not_a_number")


# === Tests archive-project ===


@patch("gitlab_monitor.commands.cli.CLICommand")
def test_archive_project_with_id(mock_cli_command):
    mock_command_instance = mock_cli_command.return_value
    mock_command_instance.create_command.return_value = MagicMock()

    result = runner.invoke(app, ["archive-project", "123"])

    assert result.exit_code == 0
    assert "Given ID : 123" in result.output
    mock_cli_command.assert_called_once()
    mock_command_instance.create_command.assert_called_once_with("archive_project")
    mock_command_instance.handle_command.assert_called_once_with(
        mock_command_instance.create_command.return_value,
        project="123",
    )


@patch("gitlab_monitor.commands.cli.CLICommand")
def test_archive_project_with_valid_path(mock_cli_command, tmp_path):
    valid_path = tmp_path / "projects.json"
    valid_path.write_text("[]")

    mock_command_instance = mock_cli_command.return_value
    mock_command_instance.create_command.return_value = MagicMock()

    result = runner.invoke(app, ["archive-project", str(valid_path)])

    assert result.exit_code == 0
    assert f"Given Path : {valid_path}" in result.output
    mock_cli_command.assert_called_once()
    mock_command_instance.create_command.assert_called_once_with("archive_project")
    mock_command_instance.handle_command.assert_called_once_with(
        mock_command_instance.create_command.return_value,
        project=str(valid_path),
    )


def test_archive_project_with_invalid_path():
    result = runner.invoke(app, ["archive-project", "invalid_path"])
    assert result.exit_code != 0
    assert "The argument must be a valid ID" in result.output


def test_archive_project_missing_argument():
    result = runner.invoke(app, ["archive-project"])
    assert result.exit_code != 0
    assert "Missing argument 'PROJECT'" in result.output
