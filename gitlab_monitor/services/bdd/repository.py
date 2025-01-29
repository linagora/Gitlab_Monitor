# # --- Copyright (c) 2024-2025 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""Interface for the repository design pattern implemented to easily interact with the database."""

import sys
from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import Optional
from typing import TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from gitlab_monitor.logger.logger import logger
from gitlab_monitor.services.bdd.models import Project
from gitlab_monitor.services.dto import CommitDTO
from gitlab_monitor.services.dto import ProjectDTO


T = TypeVar("T", CommitDTO, ProjectDTO)


class Repository(ABC, Generic[T]):
    """Interface for the repository pattern.

    :param ABC: Abstract basic class to define an interface.
    :type ABC: class
    """

    def __init__(self, session: Session):
        """Constructor

        :param session: database session.
        :type session: Session
        """
        self.session = session

    @abstractmethod
    def get_by_id(self, object_id: int) -> Optional[T]:
        """Get an object by its ID.

        :param objects_id: objects ID.
        :type objects_id: int
        :return: objects searched.
        :rtype: Optional[Type]
        """

    def create(self, object_dto: T) -> None:
        """Create a project in the database.

        :param project_dto: the project to create.
        :type project_dto: ProjectDTO
        """
        try:
            db_object = self.check_in_db(object_dto)
            if db_object:
                self.session.add(db_object)
                self.session.commit()
            else:
                self.update(object_dto)
        except SQLAlchemyError as e:
            logger.error(
                "Error while creating an object in BD. Use --verbose for more details."
            )
            logger.debug(e)
            sys.exit(1)

    @abstractmethod
    def check_in_db(self, object_dto: T) -> Optional[Project]:
        """Check if an object exists in the database.

        :param object_dto: the object to check.
        :type object_dto: T
        :return: the existing object or None.
        :rtype: Optional[T]
        """

    @abstractmethod
    def update(self, object_dto: T) -> None:
        """Update an object in the database.

        :param object_dto: the object with the updated data.
        :type object_dto: T
        """

    # @abstractmethod
    # def delete(self, object_id: int) -> None:
    #     """Delete an object in the database.

    #     :param object_id: id of the object to delete.
    #     :type object_id: int
    #     """
    #     raise NotImplementedError("Subclasses must implement this method")
