import pytest
from unittest.mock import MagicMock
from gitlab_monitor.commands.command_mapper import CommandMapper


@pytest.fixture(autouse=True)
def reset_command_mapper():
    """Fixture to reset CommandMapper._commands before each test."""
    CommandMapper._commands = {}


def test_register_command():
    """Test registering a new command."""
    mock_command = MagicMock()
    CommandMapper.register("test_command", mock_command)

    assert "test_command" in CommandMapper._commands
    assert CommandMapper._commands["test_command"] == mock_command


def test_get_existing_command():
    """Test retrieving a registered command."""
    mock_command = MagicMock()
    CommandMapper.register("test_command", mock_command)

    retrieved_command = CommandMapper.get_command("test_command")
    assert retrieved_command == mock_command


def test_get_nonexistent_command():
    """Test retrieving a non-existent command raises ValueError."""
    with pytest.raises(ValueError, match="Command nonexistent_command not found."):
        CommandMapper.get_command("nonexistent_command")


def test_register_multiple_commands():
    """Test registering multiple commands."""
    mock_command_1 = MagicMock()
    mock_command_2 = MagicMock()

    CommandMapper.register("command_1", mock_command_1)
    CommandMapper.register("command_2", mock_command_2)

    assert CommandMapper.get_command("command_1") == mock_command_1
    assert CommandMapper.get_command("command_2") == mock_command_2
