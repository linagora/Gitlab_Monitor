
# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from dto import ProjectDTO


class Mapper:
    @staticmethod
    def from_gitlab_api(self, project_data) -> ProjectDTO:
        """Recupere les valeurs de l'api pour en faire un DTO"""
        project_id = project_data.id
        name = project_data.name
        description = project_data.description
        release = project_data.release
        visibility = project_data.visibility
        created_at = project_data.created_at
        updated_at = project_data.updated_at

        return ProjectDTO(
            project_id=project_id,
            name=name,
            description=description,
            release=release,
            visibility=visibility,
            created_at=created_at,
            updated_at=updated_at,
        )
