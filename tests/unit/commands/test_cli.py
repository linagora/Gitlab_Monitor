from unittest.mock import MagicMock, patch
import pytest
import typer
from typer.testing import CliRunner

from gitlab_monitor.commands.cli import app, _version_callback, _verbose_callback
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
