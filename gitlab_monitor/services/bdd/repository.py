# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from abc import ABC
from abc import abstractmethod
from typing import Optional

from gitlab_monitor.services.dto import ProjectDTO


class Repository(ABC):
    @abstractmethod
    def get_by_id(self, project_id: int) -> Optional[ProjectDTO]:
        pass

    @abstractmethod
    def create(self, project_dto: ProjectDTO) -> None:
        pass

    @abstractmethod
    def update(self, project_dto: ProjectDTO) -> None:
        pass

    @abstractmethod
    def delete(self, project_id: int) -> None:
        pass
