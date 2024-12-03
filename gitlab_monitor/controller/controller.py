# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""
Module that contains the logic for executing commands. It retrieves information
from the controller or rather the controller sends it the information and
indicates which command to execute.

The idea here is to use a design pattern similar to the Command Pattern
to have an interface between the command line and the controller. I do not want
the controller to directly call the model tools in case the database or API
changes. User inputs should not change and this should not impact the workflow.
"""

import os
from abc import ABC
from abc import abstractmethod

from dotenv import load_dotenv

from gitlab_monitor.logger.logger import logger
from gitlab_monitor.services.bdd.bdd import Database
from gitlab_monitor.services.bdd.project_repository import (
    SQLAlchemyProjectRepository,
)
from gitlab_monitor.services.call_gitlab import GitlabAPIService
from gitlab_monitor.services.mapper import Mapper


class Command(ABC):  # pylint: disable=too-few-public-methods
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

        self.mapper = Mapper()
        self.db = Database()
        self.db._initialize_database()

        self.gitlab_service = GitlabAPIService(
            "https://ci.linagora.com", self.private_token, self.mapper, ssl_cert_path
        )
        self.project_repository = SQLAlchemyProjectRepository(self.db.session)

    @abstractmethod
    def execute(self, kwargs):
        """Define the method execute that will be implemented in the child classes."""
        raise NotImplementedError("Subclasses must implement this method")


class GetProjectsCommand(Command):  # pylint: disable=too-few-public-methods
    """Class of the command scan-projects.

    :param Command: Interface for the commands.
    :type Command: class
    """

    def execute(self):  # pylint: disable=arguments-differ
        """Execute the command scan-projects."""
        projects = self.gitlab_service.scan_projects()
        for project in projects:
            self.project_repository.create(project)
        logger.info(
            "%d projects have been retrieved and saved or updated in the database.",
            len(projects),
        )


class GetProjectCommand(Command):  # pylint: disable=too-few-public-methods
    """Class of the command scan-project.

    :param Command: Interface for the commands.
    :type Command: class
    """

    def execute(self, kwargs):
        """Execute the command scan-project [ID].

        :param id: id of the project to retrieve.
        :type id: int from kwargs in the previous methods.
        """
        project_id = kwargs.get("id")
        project = self.gitlab_service.get_project_by_id(project_id)
        if project:
            self.project_repository.create(project)
            logger.info(
                "Project %s has been retrieved and saved or updated in the database.",
                project.name,
            )
