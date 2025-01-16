# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""Module Command Mapper: used to manage commands available in gitlab_monitor.
"""

from typing import Type

from gitlab_monitor.controller.controller import GetProjectCommand
from gitlab_monitor.controller.controller import GetProjectsCommand


class CommandMapper:
    """Class CommandMapper: used to manage commands available in gitlab_monitor."""

    _commands: dict[str, Type] = {}

    @classmethod
    def register(cls, command_name: str, command_class: Type) -> None:
        """Register a command in the command mapper.

        :param command_name: name of the new command.
        :type command_name: str
        :param command_class: class of the new command.
        :type command_class: Type
        """
        cls._commands[command_name] = command_class

    @classmethod
    def get_command(cls, command_name: str) -> Type:
        """Getter for a command.

        :param command_name: name of the command to get.
        :type command_name: str
        :raises ValueError: handle the case where the command is not found.
        :return: the command class to instantiate.
        :rtype: Type
        """
        command_class = cls._commands.get(command_name)
        if not command_class:
            raise ValueError(f"Command {command_name} not found.")
        return command_class


# Enregistrement des commandes
CommandMapper.register("scan_projects", GetProjectsCommand)
CommandMapper.register("scan_project", GetProjectCommand)
