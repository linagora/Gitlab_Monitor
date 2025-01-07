# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com
"""Objects transformation module."""

from gitlab_monitor.services.bdd.models import Commit
from gitlab_monitor.services.bdd.models import Project
from gitlab_monitor.services.dto import CommitDTO
from gitlab_monitor.services.dto import ProjectDTO


class DatabaseToDTOMapper:
    """Transforms the data from the database to the objectDTO."""

    def map_project_to_dto(self, project_db: Project) -> ProjectDTO:
        """Transform the data of a project from the database to a ProjectDTO.

        :param project_db: project from the database
        :type project_db: Project
        :return: project in DTO format
        :rtype: ProjectDTO
        """
        return ProjectDTO(
            project_id=project_db.project_id,
            name=project_db.name,
            path=project_db.path,
            description=project_db.description,
            release=project_db.release,
            visibility=project_db.visibility,
            created_at=project_db.created_at,
            updated_at=project_db.updated_at,
        )

    def map_commit_to_dto(self, commit_db: Commit) -> CommitDTO:
        """Transform the data of a commit from the database to a CommitDTO.

        :param commit_db: commit from the database
        :type commit_db: Commit
        :return: commit in DTO format
        :rtype: CommitDTO
        """
        return CommitDTO(
            commit_id=commit_db.commit_id,
            project_id=commit_db.project_id,
            message=commit_db.message,
            date=commit_db.date,
            author=commit_db.author,
        )
