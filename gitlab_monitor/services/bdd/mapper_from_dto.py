"""Objects transformation module."""

from gitlab_monitor.services.bdd.models import Commit
from gitlab_monitor.services.bdd.models import Project
from gitlab_monitor.services.dto import CommitDTO
from gitlab_monitor.services.dto import ProjectDTO


class MapperFromDTO:
    """Transform DTOs objects into database models objects."""

    def project_from_dto(self, project_dto: ProjectDTO) -> Project:
        """Transform the data of a project from a ProjectDTO to a Project.

        :param project_dto: project in DTO format
        :type project_dto: ProjectDTO
        :return: project in database format
        :rtype: Project
        """
        return Project(
            project_id=project_dto.project_id,
            name=project_dto.name,
            path=project_dto.path,
            description=project_dto.description,
            release=project_dto.release,
            visibility=project_dto.visibility,
            created_at=project_dto.created_at,
            updated_at=project_dto.updated_at,
        )

    def commit_from_dto(self, commit_dto: CommitDTO) -> Commit:
        """Transform the data of a commit from a CommitDTO to a Commit.

        :param commit_dto: commit in DTO format
        :type commit_dto: CommitDTO
        :return: commit in database format
        :rtype: Commit
        """
        return Commit(
            commit_id=commit_dto.commit_id,
            project_id=commit_dto.project_id,
            message=commit_dto.message,
            date=commit_dto.date,
            author=commit_dto.author,
        )
