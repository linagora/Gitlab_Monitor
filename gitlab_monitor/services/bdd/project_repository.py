# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""
Repository pattern for the project entity.

Simple way to interact with the database for the project table.

pylint: disable=duplicate-code ; can't ignore the duplicate-code error from pylint
"""

import sys
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError

from gitlab_monitor.exc import ProjectNotFoundError
from gitlab_monitor.logger.logger import logger
from gitlab_monitor.services.bdd.mapper_from_db import DatabaseToDTOMapper
from gitlab_monitor.services.bdd.mapper_from_dto import DTOToDatabaseMapper
from gitlab_monitor.services.bdd.models import Project
from gitlab_monitor.services.bdd.repository import Repository
from gitlab_monitor.services.dto import ProjectDTO


class SQLAlchemyProjectRepository(Repository[ProjectDTO]):
    """Repository pattern for the project entity.

    :param Repository: interface implemented for the repository pattern.
    :type Repository: class
    """

    def get_by_id(self, object_id: int) -> Optional[ProjectDTO]:
        """Get a project by its ID.

        :param project_id: projet ID.
        :type project_id: int
        :return: the project searched.
        :rtype: Optional[ProjectDTO]
        """
        project = (
            self.session.query(Project).filter(Project.project_id == object_id).first()
        )
        if project:
            return DatabaseToDTOMapper().map_project_to_dto(project)
        return None

    def check_in_db(self, object_dto: ProjectDTO) -> None | Project:
        """Create a project in the database.

        :param project_dto: the project to create.
        :type project_dto: ProjectDTO
        """
        existing_project = (
            self.session.query(Project)
            .filter(Project.project_id == object_dto.project_id)
            .first()
        )
        if not existing_project:
            return DTOToDatabaseMapper().map_project_to_database(object_dto)
        return None

    def update(self, object_dto: ProjectDTO) -> None:  # pylint: disable=duplicate-code
        """Update a project in the database.

        :param project_dto: the project to update.
        :type project_dto: ProjectDTO
        :raises Exception: Raised if the project is not found.
        """
        try:
            project = (
                self.session.query(Project)
                .filter(Project.project_id == object_dto.project_id)
                .first()
            )
            if project:
                for field, data in vars(object_dto).items():
                    if hasattr(project, field):
                        setattr(project, field, data)
                self.session.commit()
            else:
                raise ProjectNotFoundError(
                    f"Project with ID {object_dto.project_id} not found"
                )
        except SQLAlchemyError as e:
            logger.error(
                "Error while updating project id : %s in BD.", object_dto.project_id
            )
            logger.debug(e)
            sys.exit(1)

    # def delete(self, object_id: int) -> None:
    #     """Delete a project in the database.

    #     :param project_id: project ID.
    #     :type project_id: int
    #     :raises Exception: Raised if the project is not found.
    #     """
    #     try:
    #         project = (
    #             self.session.query(Project)
    #             .filter(Project.project_id == object_id)
    #             .first()
    #         )
    #         if project:
    #             self.session.delete(project)
    #             self.session.commit()
    #         else:
    #             raise ProjectNotFoundError(f"Commit with ID {object_id} not found")
    #     except SQLAlchemyError as e:
    #         logger.error("Error while deleting project id : %s in BD.", object_id)
    #         logger.debug(e)
    #         sys.exit(1)
