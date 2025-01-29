# # --- Copyright (c) 2024-2025 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""Module that retrieves user inputs and sends them to the controller."""

from typing import Type

from gitlab_monitor.commands.command_mapper import CommandMapper


class CLICommand:
    """Manage the commands from the command line interface."""

    def create_command(self, command: str) -> Type:
        """Retrieve the command class from the command mapper.

        :param command: the name of the command
        :type command: str
        :return: the command class
        :rtype: Type
        """
        return CommandMapper.get_command(command)

    def handle_command(self, command_class: Type, **kwargs) -> None:
        """Declare the command and execute it from the controller.

        :param command_class: Class of the command to execute
        :type command_class: Type
        """
        command_instance = command_class(kwargs)
        if kwargs:
            command_instance.execute(kwargs)
        else:
            command_instance.execute()
