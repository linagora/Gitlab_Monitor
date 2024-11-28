# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from gitlab_monitor.controller.controller import GetProjectsCommand
from gitlab_monitor.controller.controller import GetProjectCommand


class CommandMapper:
    _commands = {}

    @classmethod
    def register(cls, command_name, command_class):
        cls._commands[command_name] = command_class

    @classmethod
    def get_command(cls, command_name):
        command_class = cls._commands.get(command_name, "Commande non reconnue")
        return command_class


CommandMapper.register("scan_projects", GetProjectsCommand)
CommandMapper.register("scan_project", GetProjectCommand)