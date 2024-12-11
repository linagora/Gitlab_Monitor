

from gitlab_monitor.services.bdd.models import Commit, Project
from gitlab_monitor.services.dto import CommitDTO, ProjectDTO


class MapperFromDTO:
    """Transform DTOs objects into database models objects."""

    def project_from_dto(self, project: ProjectDTO) -> Project:
        """Transform the data of a project from a ProjectDTO to a Project.

        :param project: project in DTO format
        :type project: ProjectDTO
        :return: project in database format
        :rtype: Project
        """
        return Project(
            project_id=project.project_id,
            name=project.name,
            path=project.path,
            description=project.description,
            release=project.release,
            visibility=project.visibility,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )
    
    def commit_from_dto(self, commit: CommitDTO) -> Commit:
        """Transform the data of a commit from a CommitDTO to a Commit.

        :param commit: commit in DTO format
        :type commit: CommitDTO
        :return: commit in database format
        :rtype: Commit
        """
        return Commit(
            commit_id=commit.commit_id,
            project_id=commit.project_id,
            message=commit.message,
            date=commit.date,
            author=commit.author,
        )