# # --- Copyright (c) 2024 Linagora
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
from sqlalchemy.orm import Session

from gitlab_monitor.exc import CommitNotFoundError
from gitlab_monitor.logger.logger import logger
from gitlab_monitor.services.bdd.models import Commit
from gitlab_monitor.services.bdd.repository import Repository
from gitlab_monitor.services.dto import CommitDTO


class SQLAlchemyCommitRepository(Repository[CommitDTO]):
    """Repository pattern for the commit entity.

    :param Repository: interface implemented for the repository pattern.
    :type Repository: class
    """

    def __init__(self, session: Session):
        """Constructor

        :param session: database session.
        :type session: Session
        """
        self.session = session

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
            return CommitDTO(
                commit_id=str(commit.commit_id),
                project_id=int(commit.project_id),
                message=str(commit.message),
            )
        return None

    def create(self, object_dto: CommitDTO) -> None:  # pylint: disable=duplicate-code
        """Create a commit in the database.

        :param commit_dto: the commit to create.
        :type commit_dto: CommitDTO
        """
        try:
            existing_commit = (
                self.session.query(Commit)
                .filter(Commit.commit_id == object_dto.commit_id)
                .first()
            )
            if not existing_commit:
                commit = Commit(
                    commit_id=object_dto.commit_id,
                    project_id=object_dto.project_id,
                    message=str(object_dto.message),
                )
                self.session.add(commit)
                self.session.commit()
            else:
                self.update(object_dto)
        except SQLAlchemyError as e:
            logger.error(
                "Error while creating commit id : %s in BD.", object_dto.commit_id
            )
            logger.debug(e)
            sys.exit(1)

    def update(self, object_dto: CommitDTO) -> None:  # pylint: disable=duplicate-code
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
                commit.project_id = object_dto.project_id
                commit.message = object_dto.message
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
