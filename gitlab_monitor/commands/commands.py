
# # --- Copyright (c) 2024 Linagora
# # licence       : GNU GENERAL PUBLIC LICENSE
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from typing import Type

from gitlab_monitor.commands.command_mapper import CommandMapper
from gitlab_monitor.controller.controller import Command


"""Module that retrieves user inputs and sends them to the controller"""


class CLICommand:
    def create_command(self, command: str):
        return CommandMapper.get_command(command)

    def handle_command(self, command_class: Type, **kwargs):
        command_instance = command_class()
        if kwargs:
            command_instance.execute(kwargs)
        else:
            command_instance.execute()
