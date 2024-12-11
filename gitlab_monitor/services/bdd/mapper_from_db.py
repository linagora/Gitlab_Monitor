

from gitlab_monitor.services.bdd.models import Commit, Project
from gitlab_monitor.services.dto import CommitDTO, ProjectDTO


class MapperFromDB:
    """Transforms the data from the database to the objectDTO."""

    def project_from_db(self, project: Project) -> ProjectDTO:
        """Transform the data of a project from the database to a ProjectDTO.

        :param project: project from the database
        :type project: Project
        :return: project in DTO format
        :rtype: ProjectDTO
        """
        return ProjectDTO(
            project_id=project.project_id,
            name=project.name,
            path=project.path,
            description=project.description,
            release=project.release,
            visibility=project.visibility,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )
    
    def commit_from_db(self, commit: Commit) -> CommitDTO:
        """Transform the data of a commit from the database to a CommitDTO.

        :param commit: commit from the database
        :type commit: Commit
        :return: commit in DTO format
        :rtype: CommitDTO
        """
        return CommitDTO(
            commit_id=commit.commit_id,
            project_id=commit.project_id,
            message=commit.message,
            date=commit.date,
            author=commit.author,
        )