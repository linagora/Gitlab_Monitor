from controller.controller import GetProjectsCommand


class CommandMapper:
    _commands = {}

    @classmethod
    def register(cls, command_name, command_class):
        cls._commands[command_name] = command_class

    @classmethod
    def get_command(cls, command_name):
        return cls._commands.get(command_name, "Commande non reconnue")


CommandMapper.register("scan_projects", GetProjectsCommand)
