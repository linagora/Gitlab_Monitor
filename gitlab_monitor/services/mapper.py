# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""This module can map data from the API to a DTO.
"""

from gitlab_monitor.services.dto import ProjectDTO


class Mapper:  # pylint: disable=too-few-public-methods
    """Transform data from the API to a DTO."""

# TODO: typer project data (json)
    def project_from_gitlab_api(self, project_data) -> ProjectDTO:
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
        created_at = project_data.created_at
        updated_at = project_data.updated_at

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
