# # --- Copyright (c) 2024 Linagora
# # licence       : GNU GENERAL PUBLIC LICENSE
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com
from typing import Optional

from sqlalchemy.orm import Session

from gitlab_monitor.services.bdd.models import Project
from gitlab_monitor.services.bdd.repository import Repository
from gitlab_monitor.services.dto import ProjectDTO


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
                project_id=int(project.project_id),
                name=project.name,
                path=project.path,
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
        except Exception as e:
            print(f"Error during project creation in DB: {e}")

    def update(self, project_dto: ProjectDTO) -> None:
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
