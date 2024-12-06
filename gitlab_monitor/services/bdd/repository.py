# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""Interface for the repository design pattern implemented to easily interact with the database."""

from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import Optional
from typing import TypeVar

from gitlab_monitor.services.dto import CommitDTO
from gitlab_monitor.services.dto import ProjectDTO


T = TypeVar("T", CommitDTO, ProjectDTO)


class Repository(ABC, Generic[T]):
    """Interface for the repository pattern.

    :param ABC: Abstract basic class to define an interface.
    :type ABC: class
    """

    @abstractmethod
    def get_by_id(self, object_id: int) -> Optional[T]:
        """Get an object by its ID.

        :param objects_id: objects ID.
        :type objects_id: int
        :return: objects searched.
        :rtype: Optional[Type]
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def create(self, object_dto: T) -> None:
        """create an objects in database.

                :param object_dto
        : objects to create.
                :type object_dto
        : Type
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def update(self, object_dto: T) -> None:
        """update an objects in database.

                :param object_dto
        : objects with the updated data.
                :type object_dto
        : Type
        """
        raise NotImplementedError("Subclasses must implement this method")

    # @abstractmethod
    # def delete(self, object_id: int) -> None:
    #     """delete an objects in database.

    #     :param objects_id: id of the objects to delete.
    #     :type objects_id: int
    #     """
    #     raise NotImplementedError("Subclasses must implement this method")
