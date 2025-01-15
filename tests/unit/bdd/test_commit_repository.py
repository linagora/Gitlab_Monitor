# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com
from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from gitlab_monitor.exc import CommitNotFoundError
from gitlab_monitor.services.bdd.bdd import Database
from gitlab_monitor.services.bdd.commit_repository import (
    SQLAlchemyCommitRepository,
)
from gitlab_monitor.services.dto import CommitDTO


@pytest.fixture
def db():
    db = MagicMock(Database)
    db._initialize_database = MagicMock()
    db.session = MagicMock()
    return db


@pytest.fixture
def commit_repository(db):
    return SQLAlchemyCommitRepository(db.session)


@pytest.fixture
def commit():
    return CommitDTO(
        commit_id="false0commit0id",
        project_id=8888,
        message="Test Commit",
        date="2021-01-01",
        author="Test Author",
    )


# ----- Tests get_by_id -----


def test_get_by_id(commit_repository, commit):
    commit_repository.session.query().filter().first.return_value = commit
    result = commit_repository.get_by_id(commit.project_id)
    assert result == commit
    commit_repository.session.query().filter().first.assert_called_once()


# ----- Tests create (method from base class repository, that call check_in_db method) -----


def test_create_commit(commit_repository, commit):
    commit_repository.session.query().filter().first.return_value = None
    commit_repository.create(commit)
    commit_repository.session.add.assert_called_once()
    commit_repository.session.commit.assert_called_once()


def test_create_commit_update(commit_repository, commit):
    commit_repository.session.query().filter().first.return_value = commit
    commit_repository.create(commit)
    commit_repository.session.add.assert_not_called()
    commit_repository.session.commit.assert_called_once()


def test_create_commit_fail(commit_repository):
    with pytest.raises(AttributeError):
        commit_repository.create("i'm not a commit")
    commit_repository.session.add.assert_not_called()
    commit_repository.session.commit.assert_not_called()


# ----- Tests update -----


def test_update_commit(commit_repository, commit):
    commit_repository.session.query().filter().first.return_value = commit
    updated_commit = CommitDTO(
        commit_id="false0commit0id",
        project_id=8888,
        message="Updated Test Commit",
        date="2021-01-01",
        author="Test Author",
    )
    commit_repository.update(updated_commit)
    commit_repository.session.commit.assert_called_once()
    assert commit.commit_id == "false0commit0id"
    assert commit.project_id == 8888
    assert commit.message == "Updated Test Commit"


def test_update_commit_not_found(commit_repository, commit):
    commit_repository.session.query().filter().first.return_value = None
    updated_commit = CommitDTO(
        commit_id="false0commit0id",
        project_id=8888,
        message="Test Commit",
        date="2021-01-01",
        author="Test Author",
    )
    with pytest.raises(CommitNotFoundError):
        commit_repository.update(updated_commit)


def test_update_commit_sqlalchemy_error(commit_repository, commit):
    commit_repository.session.query().filter().first.return_value = commit
    commit_repository.session.commit.side_effect = SQLAlchemyError("Database error")

    updated_commit = CommitDTO(
        commit_id="false0commit0id",
        project_id=8888,
        message="Test Commit",
        date="2021-01-01",
        author="Test Author",
    )

    with pytest.raises(SystemExit):
        commit_repository.update(updated_commit)

    commit_repository.session.commit.assert_called_once()
