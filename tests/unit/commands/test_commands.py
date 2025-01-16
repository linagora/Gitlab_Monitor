from unittest.mock import MagicMock, patch
from gitlab_monitor.commands.commands import CLICommand
from gitlab_monitor.commands.command_mapper import CommandMapper


def test_create_command():
    """Test the create_command method to retrieve a command class."""
    mock_command_class = MagicMock()

    with patch.object(
        CommandMapper, "get_command", return_value=mock_command_class
    ) as mock_get_command:
        cli_command = CLICommand()
        command = cli_command.create_command("test_command")

        mock_get_command.assert_called_once_with("test_command")
        assert command == mock_command_class


def test_handle_command_with_kwargs():
    """Test the handle_command method with additional arguments."""
    mock_command_class = MagicMock()
    mock_command_instance = MagicMock()

    mock_command_class.return_value = mock_command_instance

    cli_command = CLICommand()
    kwargs = {"arg1": "value1", "arg2": "value2"}

    cli_command.handle_command(mock_command_class, **kwargs)

    mock_command_class.assert_called_once_with(kwargs)
    mock_command_instance.execute.assert_called_once_with(kwargs)


def test_handle_command_without_kwargs():
    """Test the handle_command method without additional arguments."""
    mock_command_class = MagicMock()
    mock_command_instance = MagicMock()

    mock_command_class.return_value = mock_command_instance

    cli_command = CLICommand()
    cli_command.handle_command(mock_command_class)

    mock_command_class.assert_called_once_with({})
    mock_command_instance.execute.assert_called_once_with()
