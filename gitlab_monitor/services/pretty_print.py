# # --- Copyright (c) 2024-2025 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""Module for pretty printing the data retrieved from the GitLab API, when we use
the --no-database option."""

from abc import ABC
from abc import abstractmethod

from gitlab_monitor.services.dto import CommitDTO
from gitlab_monitor.services.dto import ProjectDTO


class MyPrettyPrint(ABC):
    """Base class for the pretty print service to use with the --no-datase option."""

    @abstractmethod
    def print_dto(self, dto) -> None:
        """Prints the DTO in a pretty format.

        :param dto: The data transfer object to pretty print.
        :type dto: object
        """

    def print_dto_list(self, dto_list, dto_type) -> None:
        """Prints the list of DTOs in a pretty format.

        :param dto_list: The list of data transfer objects to pretty print.
        :type dto_list: list
        """
        print("\n--------------------")
        print(f"  List of {dto_type}: ")
        print("--------------------")

        index = 0
        for dto in dto_list:
            print(f"index={index}")
            self.print_dto(dto)
            print("-" * 75)
            index += 1


class PrintProjectDTO(MyPrettyPrint):
    """Class to pretty print the ProjectDTO."""

    def print_dto(self, dto) -> None:
        """Prints the ProjectDTO in a pretty format.

        :param dto: The data transfer object to pretty print.
        :type dto: object
        """
        if not isinstance(dto, ProjectDTO):
            raise TypeError("Expected a ProjectDTO object.")

        print("\nProjectDTO:")
        print(f"  Project ID   : {dto.project_id}")
        print(f"  Name         : {dto.name}")
        print(f"  Path         : {dto.path}")
        print(f"  Description  : {dto.description}")
        print(f"  Release      : {dto.release}")
        print(f"  Visibility   : {dto.visibility}")
        print(f"  Created At   : {dto.created_at}")
        print(f"  Updated At   : {dto.updated_at}\n")


class PrintCommitDTO(MyPrettyPrint):
    """Class to pretty print the CommitDTO."""

    def print_dto(self, dto) -> None:
        """Prints the CommitDTO in a pretty format.

        :param dto: The data transfer object to pretty print.
        :type dto: object
        """
        if not isinstance(dto, CommitDTO):
            raise TypeError("Expected a CommitDTO object.")

        print("\nCommitDTO:")
        print(f"  Commit ID  : {dto.commit_id}")
        print(f"  Project ID : {dto.project_id}")
        print(f"  Message    : {dto.message}")
        print(f"  Date       : {dto.date}")
        print(f"  Author     : {dto.author}\n")
