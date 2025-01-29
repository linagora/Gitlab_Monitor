# # --- Copyright (c) 2024-2025 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""Repository pattern for the project entity.

Simple way to interact with the database for the project table.

pylint: disable=duplicate-code ; can't ignore the duplicate-code error from pylint
"""

import sys
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError

from gitlab_monitor.exc import CommitNotFoundError
from gitlab_monitor.logger.logger import logger
from gitlab_monitor.services.bdd.mapper_from_db import DatabaseToDTOMapper
from gitlab_monitor.services.bdd.mapper_from_dto import DTOToDatabaseMapper
from gitlab_monitor.services.bdd.models import Commit
from gitlab_monitor.services.bdd.repository import Repository
from gitlab_monitor.services.dto import CommitDTO


class SQLAlchemyCommitRepository(Repository[CommitDTO]):
    """Repository pattern for the commit entity.

    :param Repository: interface implemented for the repository pattern.
    :type Repository: class
    """

    def get_by_id(self, object_id: int) -> Optional[CommitDTO]:
        """Get a commit by its ID.

        :param commit_id: commit ID.
        :type commit_id: int
        :return: the commit searched.
        :rtype: Optional[CommitDTO]
        """
        commit = (
            self.session.query(Commit).filter(Commit.commit_id == object_id).first()
        )
        if commit:
            return DatabaseToDTOMapper().map_commit_to_dto(commit)
        return None

    def check_in_db(self, object_dto: CommitDTO) -> Optional[Commit]:
        """Create a commit in the database.

        :param commit_dto: the commit to create.
        :type commit_dto: CommitDTO
        """
        existing_commit = (
            self.session.query(Commit)
            .filter(Commit.commit_id == object_dto.commit_id)
            .first()
        )
        if not existing_commit:
            return DTOToDatabaseMapper().map_commit_to_database(object_dto)
        return None

    def update(self, object_dto: CommitDTO) -> None:
        """Update a commit in the database.

        :param commit_dto: the commit to update.
        :type commit_dto: CommitDTO
        :raises Exception: Raised if the commit is not found.
        """
        try:
            commit = (
                self.session.query(Commit)
                .filter(Commit.commit_id == object_dto.commit_id)
                .first()
            )
            if commit:
                for field, data in vars(object_dto).items():
                    if hasattr(commit, field):
                        setattr(commit, field, data)
                self.session.commit()
            else:
                raise CommitNotFoundError(
                    f"Commit with ID {object_dto.commit_id} not found"
                )
        except SQLAlchemyError as e:
            logger.error(
                "Error while updating commit id : %s in BD.", object_dto.commit_id
            )
            logger.debug(e)
            sys.exit(1)

    # def delete(self, object_id: str) -> None:
    #     """Delete a commit in the database.

    #     :param commit_id: commit ID.
    #     :type commit_id: str
    #     :raises Exception: Raised if the commit is not found.
    #     """
    #     try:
    #         commit = (
    #             self.session.query(Commit).filter(Commit.commit_id == object_id).first()
    #         )
    #         if commit:
    #             self.session.delete(commit)
    #             self.session.commit()
    #         else:
    #             raise CommitNotFoundError(f"Commit with ID {object_id} not found")
    #     except SQLAlchemyError as e:
    #         logger.error("Error while deleting commit id : %s in BD.", object_id)
    #         logger.debug(e)
    #         sys.exit(1)
