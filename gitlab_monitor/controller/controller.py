# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""
Module for executing commands and interfacing between the command line and the controller.
Ensures user inputs remain consistent even if the database or API changes.
"""

import os
from abc import ABC
from abc import abstractmethod

from dotenv import load_dotenv
from gitlab.base import RESTObject

from gitlab_monitor.logger.logger import logger
from gitlab_monitor.services.bdd.bdd import Database
from gitlab_monitor.services.bdd.commit_repository import (
    SQLAlchemyCommitRepository,
)
from gitlab_monitor.services.bdd.project_repository import (
    SQLAlchemyProjectRepository,
)
from gitlab_monitor.services.call_gitlab import GitlabAPIService
from gitlab_monitor.services.dto import CommitDTO
from gitlab_monitor.services.dto import ProjectDTO
from gitlab_monitor.services.mapper import Mapper
from gitlab_monitor.services.pretty_print import PrintCommitDTO
from gitlab_monitor.services.pretty_print import PrintProjectDTO


class Command(ABC):
    """Interface for the commands.

    :param ABC: Abstract Base Classes
    :type ABC: class
    """

    def __init__(self) -> None:
        """Constructor of the Command class.

        :raises ValueError: Handle error from the environment variables.
        """
        load_dotenv()
        self.private_token = os.getenv("GITLAB_PRIVATE_TOKEN")
        if not self.private_token:
            raise ValueError(
                "GITLAB_PRIVATE_TOKEN is not set in the environment variables"
            )
        ssl_cert_path = os.getenv("SSL_CERT_PATH")

        self.db = Database()
        self.db._initialize_database()

        self.gitlab_service = GitlabAPIService(
            "https://ci.linagora.com", self.private_token, ssl_cert_path
        )
        self.project_repository = SQLAlchemyProjectRepository(self.db._session)
        self.commit_repository = SQLAlchemyCommitRepository(self.db._session)
        self._no_db = False

    @abstractmethod
    def execute(self, kwargs):
        """Define the method execute that will be implemented in the child classes."""

    def golab_options(self, kwargs):
        """Method used to reteieve global options (options that can be used with all
        commands) from the command line."""
        self._no_db = kwargs.get("no_db")


class GetProjectsCommand(Command):
    """Class of the command scan-projects.

    :param Command: Interface for the commands.
    :type Command: class
    """

    def execute(self, kwargs):
        """Execute the command scan-projects."""

        self.golab_options(kwargs)

        projects = self.gitlab_service.scan_projects()
        projects_dto = []
        for project in projects:
            project_dto = Mapper().project_from_gitlab_api(project)
            projects_dto.append(project_dto)

        if self._no_db:
            PrintProjectDTO().print_dto_list(projects_dto, "Projects")
        else:
            self._save_projects(projects_dto)

    def _save_projects(self, projects_dto: list[ProjectDTO]) -> None:
        """Save projects in DB.

        :param projects_dto: list of projects to save
        :type projects_dto: list[ProjectDTO]
        """
        for project_dto in projects_dto:
            self.project_repository.create(project_dto)
        logger.info(
            "%d projects have been retrieved and saved or updated in the database.",
            len(projects_dto),
        )


class GetProjectCommand(Command):
    """Class of the command scan-project.

    :param Command: Interface for the commands.
    :type Command: class
    """

    def execute(self, kwargs) -> None:
        """Execute the command scan-project [ID].

        :param id: id of the project to retrieve.
        :type id: int from kwargs in the previous methods.
        """
        # Retrieve arguments from the command line
        project_id = kwargs.get("id")

        # Retrieve options from the command line
        get_commits = kwargs.get("get_commits")
        self.golab_options(kwargs)

        # Original command comportment : retrieve project and save (or updated) it in the database
        project = self.gitlab_service.get_project_by_id(project_id)
        dto_project = Mapper().project_from_gitlab_api(project)

        if self._no_db:
            PrintProjectDTO().print_dto(dto_project)
        else:
            self._save_project(dto_project)

        # Handle options: call the according method for each
        if get_commits:
            self._get_commits(project_id, project)

    def _save_project(self, dto_project: ProjectDTO) -> None:
        """Save projects in DB.

        :param dto_project: proiect to save
        :type dto_project: ProjectDTO
        """
        self.project_repository.create(dto_project)
        logger.info(
            "Project %s has been retrieved and saved or updated in the database.",
            dto_project.name,
        )

    def _get_commits(
        self, project_id: int, project_restobject_data: RESTObject
    ) -> None:
        """Retrieve commits from a project and transform them into DTOs.

        :param project_id: id of the project from which we retrieve the commits.
        :type project_id: int
        :param project_restobject_data: project from which we retrieve the commits.
        :type project_restobject_data: RESTObject
        """
        project_commits: list[RESTObject] = self.gitlab_service.get_project_commit(
            project_restobject_data
        )

        if project_commits:
            dto_commits_list = []
            for commit in project_commits:
                dto_commits_list.append(
                    Mapper().commit_from_gitlab_api(commit, project_id)
                )
            if self._no_db:
                PrintCommitDTO().print_dto_list(dto_commits_list, "Commits")
            else:
                self._save_commits(dto_commits_list, project_restobject_data)

    def _save_commits(
        self, dto_commits_list: list[CommitDTO], project_restobject_data: RESTObject
    ) -> None:
        """Save commits in DB.

        :param dto_commits_list: list of commits to save
        :type dto_commits_list: list[CommitDTO]
        :param project_restobject_data: project from which we retrieve the commits.
        :type project_restobject_data: RESTObject
        """
        for dto_commit in dto_commits_list:
            self.commit_repository.create(dto_commit)
        logger.info(
            '%d commits from project "%s" have been retrieved and saved or updated \
                in the database.',
            len(dto_commits_list),
            project_restobject_data.name,
        )
