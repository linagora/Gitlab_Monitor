
# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com










from command_mapper import CommandMapper
from controller.controller import Command
from services.bdd import Database
from services.call_gitlab import GitlabAPIService
from services.repository import SQLAlchemyProjectRepository

"""Module qui va récupérer les entrées utilisateurs puis les envoyer au module controller"""


class CLICommand:
    def create_command(self, command: str):
        return CommandMapper.get_command(command)

    def handle_command(self, command_class: Command):
        command_class.execute()
