# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""This module can map data from the API to a DTO.
"""

from datetime import datetime
from gitlab.base import RESTObject

from gitlab_monitor.services.dto import CommitDTO
from gitlab_monitor.services.dto import ProjectDTO


class Mapper:
    """Transform data from the API to a DTO."""

    def project_from_gitlab_api(self, project_data: RESTObject) -> ProjectDTO:
        """Transform the data of a gitlab project from the
        gitlab API to a ProjectDTO.

        :param project_data: project data from the gitlab API
        :type project_data: json
        :return: project in DTO format
        :rtype: ProjectDTO
        """
        project_id = project_data.id
        name = project_data.name
        path = project_data.path_with_namespace
        description = project_data.description
        release = project_data.releases_access_level
        visibility = project_data.visibility
        created_at = datetime.fromisoformat(project_data.created_at)
        updated_at = datetime.fromisoformat(project_data.updated_at)

        return ProjectDTO(
            project_id=project_id,
            name=name,
            path=path,
            description=description,
            release=release,
            visibility=visibility,
            created_at=created_at,
            updated_at=updated_at,
        )

    def commit_from_gitlab_api(
        self, commit_data: RESTObject, commit_details: RESTObject
    ) -> CommitDTO:
        """Transform the data of a gitlab commit from the
        gitlab API to a CommitDTO.

        :param project_data: project data from the gitlab API
        :type project_data: json
        :return: project in DTO format
        :rtype: ProjectDTO
        """
        commit_id = commit_data.id
        message = commit_data.title
        project_id = commit_details.project_id
        date = datetime.fromisoformat(commit_details.authored_date)
        author = commit_details.author_name

        return CommitDTO(
            commit_id=commit_id,
            message=message,
            project_id=project_id,
            date=date,
            author=author,
        )
