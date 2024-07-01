from abc import ABC, abstractmethod
from typing import List, Optional

from dto import ProjectDTO
from models import Project
from sqlalchemy.orm import Session


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


class SQLAlchemyProjectRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, project_id: int) -> Optional[ProjectDTO]:
        # Implémentation pour récupérer un projet par son ID
        project = (
            self.session.query(Project).filter(Project.project_id == project_id).first()
        )
        if project:
            return ProjectDTO(
                project_id=project.project_id,
                name=project.name,
                description=project.description,
                release=project.release,
                visibility=project.visibility,
                created_at=project.created_at,
                updated_at=project.updated_at,
            )
        else:
            return None

    def create(self, project_dto: ProjectDTO) -> None:
        # Implémentation pour créer un nouveau projet
        existing_project = (
            self.session.query(Project)
            .filter(Project.project_id == project_dto.project_id)
            .first()
        )
        if not existing_project:
            project = Project(
                project_id=project_dto.project_id,
                name=project_dto.name,
                description=project_dto.description,
                release=project_dto.release,
                visibility=project_dto.visibility,
                created_at=project_dto.created_at,
                updated_at=project_dto.updated_at,
            )
        self.session.add(project)
        self.session.commit()

    def update(self, project_dto: ProjectDTO) -> None:
        project = (
            self.session.query(Project)
            .filter(Project.project_id == project_dto.project_id)
            .first()
        )
        if project:
            project.name = project_dto.name
            project.description = project_dto.description
            project.release = project_dto.release
            project.visibility = project_dto.visibility
            project.updated_at = project_dto.updated_at
            self.session.commit()
        else:
            raise Exception("Project not found")

    def delete(self, project_id: int) -> None:
        project = (
            self.session.query(Project).filter(Project.project_id == project_id).first()
        )
        if project:
            self.session.delete(project)
            self.session.commit()
        else:
            raise Exception("Project not found")
