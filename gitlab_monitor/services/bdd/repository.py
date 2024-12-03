# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""Interface for the repository design pattern implemented to easily interact with the database."""

from abc import ABC
from abc import abstractmethod
from typing import Optional

from gitlab_monitor.services.dto import ProjectDTO


class Repository(ABC):
    """Interface for the repository pattern.

    :param ABC: Abstract basic class to define an interface.
    :type ABC: class
    """

    @abstractmethod
    def get_by_id(self, project_id: int) -> Optional[ProjectDTO]:
        """Get a project by its ID.

        :param project_id: project ID.
        :type project_id: int
        :return: project searched.
        :rtype: Optional[ProjectDTO]
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def create(self, project_dto: ProjectDTO) -> None:
        """create a project in database.

        :param project_dto: project to create.
        :type project_dto: ProjectDTO
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def update(self, project_dto: ProjectDTO) -> None:
        """update a project in database.

        :param project_dto: project with the updated data.
        :type project_dto: ProjectDTO
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def delete(self, project_id: int) -> None:
        """delete a project in database.

        :param project_id: id of the project to delete.
        :type project_id: int
        """
        raise NotImplementedError("Subclasses must implement this method")
