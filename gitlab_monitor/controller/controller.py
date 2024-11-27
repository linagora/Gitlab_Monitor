# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

import os
from abc import ABC, abstractmethod


from gitlab_monitor.services.mapper import Mapper
from gitlab_monitor.services.call_gitlab import GitlabAPIService
from gitlab_monitor.services.bdd.project_repository import SQLAlchemyProjectRepository
from gitlab_monitor.services.bdd.bdd import Database

from dotenv import load_dotenv


"""Module qui va contenir la logique d'execution des commandes, elle récupère les 
infos depuis le controller ou plutot le controller lui envoie les infos et 
indique quelle commande executer

L'idée ici est d'utiliser un design pattern qui va ressembler au Command Pattern
pour avoir une interface entre la ligne de commande et le controller, je ne souhaite
pas que le controller puisse directement appelé les outils modèles dans le cas ou 
la bdd devrait changer ou l'api devrait changer, les entrées utilisateurs ne
doivent pas changer et cela ne doit pas impacter le flux de travail.

"""


# class Controller():
#     def __init__(self):
#         load_dotenv()
#         private_token = os.getenv("GITLAB_PRIVATE_TOKEN")
#         mapper = Mapper()
#         db = Database()
#         db._initialize_database()

#         self.gitlab = GitlabAPIService("https://ci.linagora.com", private_token, mapper)
#         self.repository = SQLAlchemyProjectRepository(db.session)

#     def scan_projects(self):
#         projects = self.gitlab.scan_projects()
#         for project in projects:
#             print(project)
#             self.repository.create(project)

#     def scan_project(self, project_id):
#         project = self.gitlab.get_project_by_id(project_id)
#         print(project)
#         self.repository.create(project)

class Command(ABC):
    @abstractmethod
    def execute():
        pass


class GetProjectsCommand(Command):
    def __init__(self
    ) -> None:
        load_dotenv()
        self.private_token = os.getenv("GITLAB_PRIVATE_TOKEN")
        self.mapper = Mapper()
        self.db = Database()
        self.db._initialize_database()

        self.gitlab_service = GitlabAPIService("https://ci.linagora.com", self.private_token, self.mapper)
        self.project_repository = SQLAlchemyProjectRepository(self.db.session)

    def execute(self):
        projects = self.gitlab_service.scan_projects()
        for project in projects:
            self.project_repository.create(project)