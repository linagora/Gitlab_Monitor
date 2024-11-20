
# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from abc import ABC
from abc import abstractmethod

from containers import Container
from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from services.call_gitlab import GitlabAPIService
from services.repository import SQLAlchemyProjectRepository


"""Module qui va contenir la logique d'execution des commandes, elle récupère les 
infos depuis le controller ou plutot le controller lui envoie les infos et 
indique qu'elle commande executer

L'idée ici est d'utiliser un design pattern qui va ressembler au Command Pattern
pour avoir une interface entre la ligne de commande et le controller, je ne souhaite
pas que le controller puisse directement appelé les outils modèles dans le cas ou 
la bdd devrait changer ou l'api devrait changer, les entrées utilisateurs ne
doivent pas changer et cela ne doit pas impacter le flux de travail.

"""


class Command(ABC):
    @abstractmethod
    def execute():
        pass


class GetProjectsCommand(Command):
    @inject
    def __init__(
        self,
        gitlab_service: GitlabAPIService = Provide[Container.gitlab_service],
        project_repository: SQLAlchemyProjectRepository = Provide[
            Container.project_repository
        ],
    ) -> None:
        self.gitlab_service = gitlab_service
        self.project_repository = project_repository

    def execute(self, gitlab_service: GitlabAPIService):
        projects = gitlab_service.scan_projects()
        for project in projects:
            self.project_repository.create(project)
