# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


"""
Module that contains the business logic for calling the GitLab API.
Project is supposed to be my DTO.
"""

import sys
from requests.exceptions import ConnectionError
from typing import Optional

import gitlab

from gitlab_monitor.logger.logger import logger
from gitlab_monitor.services.dto import ProjectDTO
from gitlab_monitor.services.mapper import Mapper


class GitlabAPIService:
    """Service that calls the GitLab API."""

    def __init__(
        self,
        url: str,
        private_token: str,
        mapper: Mapper,
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
        self._mapper = mapper

    # TODO: Handle wrong data ? (no id or name)
    def scan_projects(self) -> list:
        """Retrieve all projects from the GitLab instance and convert them to DTOs.

        :return: _description_
        :rtype: list of Project in DTO format
        """
        logger.info("Retrieving projects...")
        try:
            if self._gitlab_instance.ssl_verify is False:
                logger.warning("SSL verification is not enabled. Connecting to Gitlab instance without certificate.")
            projects = self._gitlab_instance.projects.list(iterator=True)
        except ConnectionError as e:
            logger.error("Error when retrieving projects due to bad url: %s", self._gitlab_instance.url)
            logger.debug(e)
            # sys.exit(1)
            raise
        except gitlab.exceptions.GitlabAuthenticationError as e:
            logger.error("Authentication error due to bad token: %s", self._gitlab_instance.private_token)
            logger.debug(e)
            raise
        except OSError as e:
            logger.error("Wrong path to gitlab authentifcation certificate: %s", self._gitlab_instance.ssl_verify)
            logger.debug(e)
            raise

        projects_dto = []
        for project in projects:
            project_dto = self._mapper.project_from_gitlab_api(project)
            projects_dto.append(project_dto)
        return projects_dto

    def get_project_by_id(self, project_id) -> Optional[ProjectDTO]:
        """Get a project from gitlab by its id.

        :param project_id: project id
        :type project_id: int from kwargs
        :return: the project searched in DTO format
        :rtype: ProjectDTO
        """
        logger.info("Retrieving project id %s...", project_id)
        try:
            if self._gitlab_instance.ssl_verify is True:
                logger.warning("SSL verification is not enabled. Connecting to Gitlab instance without certificate.")            
            project = self._gitlab_instance.projects.get(project_id)
            return self._mapper.project_from_gitlab_api(project)
        except ConnectionError as e:
            logger.error("Error when retrieving projects due to bad url: %s", self._gitlab_instance.url)
            logger.debug(e)
            raise
        except gitlab.exceptions.GitlabAuthenticationError as e:
            logger.error("Authentication error due to bad token: %s", self._gitlab_instance.private_token)
            logger.debug(e)
            raise
        except OSError as e:
            logger.error("Wrong path to gitlab authentifcation certificate: %s", self._gitlab_instance.ssl_verify)
            logger.debug(e)
            raise
        except gitlab.GitlabGetError as e:
            logger.error("Error when retrieving project id %s", project_id)
            logger.debug(e)
            raise
