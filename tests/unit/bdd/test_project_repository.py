# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com
from unittest.mock import MagicMock
from unittest.mock import Mock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from gitlab_monitor.exc import ProjectNotFoundError
from gitlab_monitor.services.bdd.bdd import Database
from gitlab_monitor.services.bdd.project_repository import (
    SQLAlchemyProjectRepository,
)
from gitlab_monitor.services.dto import ProjectDTO


@pytest.fixture
def db():
    db = MagicMock(Database)
    db._initialize_database = MagicMock()
    db.session = MagicMock()
    return db


@pytest.fixture
def project_repository(db):
    return SQLAlchemyProjectRepository(db.session)


@pytest.fixture
def project():
    return ProjectDTO(
        project_id=8888,
        name="TEST UNITAIRE",
        path="test/path",
        description="Test Description",
        release="enabled",
        visibility="private",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
    )


# ----- Tests get_by_id -----


def test_get_by_id(project_repository, project):
    project_repository.session.query().filter().first.return_value = project
    result = project_repository.get_by_id(project.project_id)
    assert result == project
    project_repository.session.query().filter().first.assert_called_once()


# ----- Tests create (method from base class repository, that call check_in_db method) -----


def test_create_project(project_repository, project):
    project_repository.session.query().filter().first.return_value = None
    project_repository.create(project)
    project_repository.session.add.assert_called_once()
    project_repository.session.commit.assert_called_once()


def test_create_project_update(project_repository, project):
    project_repository.session.query().filter().first.return_value = project
    project_repository.create(project)
    project_repository.session.add.assert_not_called()
    project_repository.session.commit.assert_called_once()


def test_create_project_fail(project_repository):
    with pytest.raises(AttributeError):
        project_repository.create("i'm not a project")
    project_repository.session.add.assert_not_called()
    project_repository.session.commit.assert_not_called()


# ----- Tests update -----


def test_update_project(project_repository, project):
    project_repository.session.query().filter().first.return_value = project
    updated_project = ProjectDTO(
        project_id=8888,
        name="UPDATED TEST",
        path="updated/path",
        description="Updated Description",
        release="disabled",
        visibility="public",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-02T00:00:00Z",
    )
    project_repository.update(updated_project)
    project_repository.session.commit.assert_called_once()
    assert project.name == "UPDATED TEST"
    assert project.path == "updated/path"
    assert project.description == "Updated Description"
    assert project.release == "disabled"
    assert project.visibility == "public"
    assert project.updated_at == "2024-01-02T00:00:00Z"


def test_update_project_not_found(project_repository, project):
    project_repository.session.query().filter().first.return_value = None
    updated_project = ProjectDTO(
        project_id=8888,
        name="UPDATED TEST",
        path="updated/path",
        description="Updated Description",
        release="disabled",
        visibility="public",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-02T00:00:00Z",
    )
    with pytest.raises(ProjectNotFoundError):
        project_repository.update(updated_project)


def test_update_project_sqlalchemy_error(project_repository, project):
    project_repository.session.query().filter().first.return_value = project
    project_repository.session.commit.side_effect = SQLAlchemyError("Database error")

    updated_project = ProjectDTO(
        project_id=8888,
        name="UPDATED TEST",
        path="updated/path",
        description="Updated Description",
        release="disabled",
        visibility="public",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-02T00:00:00Z",
    )

    with pytest.raises(SystemExit):
        project_repository.update(updated_project)

    project_repository.session.commit.assert_called_once()


# ----- Tests delete - Not implemented yet -----

# def test_delete_project(project_repository, project):
#     project_repository.session.query().filter().first.return_value = project
#     project_repository.delete(project.project_id)
#     project_repository.session.delete.assert_called_once_with(project)
#     project_repository.session.commit.assert_called_once()
