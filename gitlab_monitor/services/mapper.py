# # --- Copyright (c) 2024 Linagora
# # licence       : GNU GENERAL PUBLIC LICENSE
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from gitlab_monitor.services.dto import ProjectDTO


class Mapper:
    @staticmethod
    def from_gitlab_api(self, project_data) -> ProjectDTO:
        """Recupere les valeurs de l'api pour en faire un DTO"""
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
