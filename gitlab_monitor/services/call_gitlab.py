# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


"""
Module that contains the business logic for calling the GitLab API.
Project is supposed to be my DTO.

pylint: disable redefined-builtin to avoid this error: W0622: Redefining built-in
'ConnectionError'. ConnectionError is redefine to use the
requests.exceptions.ConnectionError instead of the built-in one.
"""

import sys
from typing import Optional

import gitlab
from gitlab.base import RESTObject
from gitlab.base import RESTObjectList
from requests.exceptions import (
    ConnectionError,
)

from gitlab_monitor.logger.logger import logger


class GitlabAPIService:
    """Service that calls the GitLab API."""

    def __init__(
        self,
        url: str,
        private_token: str,
        ssl_cert_path: Optional[str] = None,
    ) -> None:
        """Constructor for the GitlabAPIService.

        :param url: url of the GitLab instance
        :type url: str
        :param private_token: personal access token for the GitLab instance.
        :type private_token: str
        :param mapper: Mapper object to map the GitLab API response to the DTO.
        :type mapper: Mapper
        :param ssl_cert_path:  path to the certificate for the GitLab instance, defaults to None
        :type ssl_cert_path: Optional[str], optional
        """
        self._gitlab_instance = gitlab.Gitlab(
            url=url,
            private_token=private_token,
            ssl_verify=ssl_cert_path if ssl_cert_path else False,
        )

    def scan_projects(self) -> RESTObjectList | list[RESTObject]:
        """Retrieve all projects from the GitLab instance and convert them to DTOs.

        :return: _description_
        :rtype: list of Project in DTO format
        """
        logger.info("Retrieving projects...")
        try:
            if self._gitlab_instance.ssl_verify is False:
                logger.warning(
                    "SSL verification is not enabled. \
                    Connecting to Gitlab instance without certificate."
                )
            return self._gitlab_instance.projects.list(iterator=True)
        except ConnectionError as e:
            logger.error(
                "Error when retrieving projects due to bad url: %s",
                self._gitlab_instance.url,
            )
            logger.debug(e)
            sys.exit(1)
        except gitlab.exceptions.GitlabAuthenticationError as e:
            logger.error(
                "Authentication error due to bad token: %s",
                self._gitlab_instance.private_token,
            )
            logger.debug(e)
            sys.exit(1)
        except OSError as e:
            logger.error(
                "Wrong path to gitlab authentifcation certificate: %s",
                self._gitlab_instance.ssl_verify,
            )
            logger.debug(e)
            sys.exit(1)

    def get_project_by_id(self, project_id: int) -> RESTObject:
        """Get a project from gitlab by its id.

        :param project_id: project id
        :type project_id: int from kwargs
        :return: the project searched
        :rtype: RESTObject (or Project from gitlab library)
        """
        logger.info("Retrieving project id %s...", project_id)
        try:
            if self._gitlab_instance.ssl_verify is True:
                logger.warning(
                    "SSL verification is not enabled. \
                    Connecting to Gitlab instance without certificate."
                )
            return self._gitlab_instance.projects.get(project_id)
        except ConnectionError as e:
            logger.error(
                "Error when retrieving projects due to bad url: %s",
                self._gitlab_instance.url,
            )
            logger.debug(e)
            sys.exit(1)
        except gitlab.exceptions.GitlabAuthenticationError as e:
            logger.error(
                "Authentication error due to bad token: %s",
                self._gitlab_instance.private_token,
            )
            logger.debug(e)
            sys.exit(1)
        except OSError as e:
            logger.error(
                "Wrong path to gitlab authentifcation certificate: %s",
                self._gitlab_instance.ssl_verify,
            )
            logger.debug(e)
            sys.exit(1)
        except gitlab.GitlabGetError as e:
            logger.error("Error when retrieving project id %s, not found.", project_id)
            logger.debug(e)
            sys.exit(1)

    def get_project_commit(self, project: RESTObject) -> list[RESTObject]:
        """Get all the commits of a project.

        :param project: project to get the commits from
        :type project: RESTObject
        :return: RESTObject of the commits
        :rtype: Optional[RESTObject]
        """
        logger.info("Retrieving commits from %s project...", project.name)
        try:
            return project.commits.list(get_all=True, all=True)
        except gitlab.GitlabGetError as e:
            logger.error("Error when retrieving commit from project %s", project.name)
            logger.debug(e)
            sys.exit(1)

    def get_commit_details(self, project: RESTObject, commit_id: str) -> RESTObject:
        """Get details of a commit by its id."""
        try:
            return project.commits.get(commit_id)
        except gitlab.GitlabGetError as e:
            logger.error(
                "Error when retrieving commit details from project %s", project.name
            )
            logger.debug(e)
            sys.exit(1)
