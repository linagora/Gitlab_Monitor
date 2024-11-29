# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

from typing import Type

from gitlab_monitor.controller.controller import GetProjectCommand
from gitlab_monitor.controller.controller import GetProjectsCommand


class CommandMapper:
    _commands: dict[str, Type] = {}

    @classmethod
    def register(cls, command_name: str, command_class: Type) -> None:
        cls._commands[command_name] = command_class

    @classmethod
    def get_command(cls, command_name: str) -> Type:
        command_class = cls._commands.get(command_name, "Commande non reconnue")
        return command_class


# Enregistrement des commandes
CommandMapper.register("scan_projects", GetProjectsCommand)
CommandMapper.register("scan_project", GetProjectCommand)
