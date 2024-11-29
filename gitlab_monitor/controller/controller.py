# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

import os
from abc import ABC
from abc import abstractmethod

from dotenv import load_dotenv

from gitlab_monitor.services.bdd.bdd import Database
from gitlab_monitor.services.bdd.project_repository import (
    SQLAlchemyProjectRepository,
)
from gitlab_monitor.services.call_gitlab import GitlabAPIService
from gitlab_monitor.services.mapper import Mapper


"""Module qui va contenir la logique d'execution des commandes, elle récupère les 
infos depuis le controller ou plutot le controller lui envoie les infos et 
indique quelle commande executer

L'idée ici est d'utiliser un design pattern qui va ressembler au Command Pattern
pour avoir une interface entre la ligne de commande et le controller, je ne souhaite
pas que le controller puisse directement appelé les outils modèles dans le cas ou 
la bdd devrait changer ou l'api devrait changer, les entrées utilisateurs ne
doivent pas changer et cela ne doit pas impacter le flux de travail.

"""


class Command(ABC):
    def __init__(self) -> None:
        load_dotenv()
        self.private_token = os.getenv("GITLAB_PRIVATE_TOKEN")
        if not self.private_token:
            raise ValueError(
                "GITLAB_PRIVATE_TOKEN is not set in the environment variables"
            )
        ssl_cert_path = os.getenv("SSL_CERT_PATH")

        self.mapper = Mapper()
        self.db = Database()
        self.db._initialize_database()

        self.gitlab_service = GitlabAPIService(
            "https://ci.linagora.com", self.private_token, self.mapper, ssl_cert_path
        )
        self.project_repository = SQLAlchemyProjectRepository(self.db.session)

    @abstractmethod
    def execute(self, **kwargs):
        pass


class GetProjectsCommand(Command):
    def execute(self):
        projects = self.gitlab_service.scan_projects()
        for project in projects:
            self.project_repository.create(project)
        print(
            f"{len(projects)} projects has been retrieved and saved or updated in database."
        )


class GetProjectCommand(Command):
    def execute(self, id):
        project_id = id.get("id")
        project = self.gitlab_service.get_project_by_id(project_id)
        if project:
            self.project_repository.create(project)
            print(
                f"Project {project.name} has been retrieved and saved or updated in database."
            )
