# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""Repository pattern for the project entity.

Simple way to interact with the database for the project table.
"""
import sys
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from gitlab_monitor.exc import ProjectNotFoundError
from gitlab_monitor.logger.logger import logger
from gitlab_monitor.services.bdd.models import Project
from gitlab_monitor.services.bdd.repository import Repository
from gitlab_monitor.services.dto import ProjectDTO


class SQLAlchemyProjectRepository(Repository):
    """Repository pattern for the project entity.

    :param Repository: interface implemented for the repository pattern.
    :type Repository: class
    """

    def __init__(self, session: Session):
        """Constructor

        :param session: database session.
        :type session: Session
        """
        self.session = session

    def get_by_id(self, project_id: int) -> Optional[ProjectDTO]:
        """Get a project by its ID.

        :param project_id: projet ID.
        :type project_id: int
        :return: the project searched.
        :rtype: Optional[ProjectDTO]
        """
        project = (
            self.session.query(Project).filter(Project.project_id == project_id).first()
        )
        if project:
            return ProjectDTO(
                project_id=int(project.project_id),
                name=project.name,
                path=project.path,
                description=project.description,
                release=project.release,
                visibility=project.visibility,
                created_at=project.created_at,
                updated_at=project.updated_at,
            )
        return None

    def create(self, project_dto: ProjectDTO) -> None:
        """Create a project in the database.

        :param project_dto: the project to create.
        :type project_dto: ProjectDTO
        """
        try:
            existing_project = (
                self.session.query(Project)
                .filter(Project.project_id == project_dto.project_id)
                .first()
            )
            if not existing_project:
                project = Project(
                    project_id=project_dto.project_id,
                    name=project_dto.name,
                    path=project_dto.path,
                    description=project_dto.description,
                    release=project_dto.release,
                    visibility=project_dto.visibility,
                    created_at=project_dto.created_at,
                    updated_at=project_dto.updated_at,
                )
                self.session.add(project)
                self.session.commit()
            else:
                self.update(project_dto)
        except SQLAlchemyError as e:
            logger.error(
                "Error while creating project id : %s in BD.", project_dto.project_id
            )
            logger.debug(e)
            sys.exit(1)

    def update(self, project_dto: ProjectDTO) -> None:
        """Update a project in the database.

        :param project_dto: the project to update.
        :type project_dto: ProjectDTO
        :raises Exception: Raised if the project is not found.
        """
        try:
            project = (
                self.session.query(Project)
                .filter(Project.project_id == project_dto.project_id)
                .first()
            )
            if project:
                project.name = project_dto.name
                project.path = project_dto.path
                project.description = project_dto.description
                project.release = project_dto.release
                project.visibility = project_dto.visibility
                project.updated_at = project_dto.updated_at
                self.session.commit()
            else:
                raise ProjectNotFoundError(
                    f"Project with ID {project_dto.project_id} not found"
                )
        except SQLAlchemyError as e:
            logger.error(
                "Error while updating project id : %s in BD.", project_dto.project_id
            )
            logger.debug(e)
            sys.exit(1)

    def delete(self, project_id: int) -> None:
        """Delete a project in the database.

        :param project_id: project ID.
        :type project_id: int
        :raises Exception: Raised if the project is not found.
        """
        try:
            project = (
                self.session.query(Project)
                .filter(Project.project_id == project_id)
                .first()
            )
            if project:
                self.session.delete(project)
                self.session.commit()
            else:
                raise ProjectNotFoundError(f"Commit with ID {project_id} not found")
        except SQLAlchemyError as e:
            logger.error("Error while deleting project id : %s in BD.", project_id)
            logger.debug(e)
            sys.exit(1)
