
# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

from unittest.mock import MagicMock
from unittest.mock import Mock

import pytest

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
    project_repository.create("i'm not a project")
    project_repository.session.add.assert_not_called()
    project_repository.session.commit.assert_not_called()
