from unittest.mock import MagicMock
from datetime import datetime

from gitlab_monitor.services.mapper import Mapper
from gitlab_monitor.services.dto import ProjectDTO, CommitDTO


def test_project_from_gitlab_api():
    project_data = MagicMock()
    project_data.id = 1
    project_data.name = "Project 1"
    project_data.path_with_namespace = "namespace/project1"
    project_data.description = "A sample project"
    project_data.releases_access_level = "enabled"
    project_data.visibility = "public"
    project_data.created_at = "2024-01-01T00:00:00Z"
    project_data.updated_at = "2024-01-02T00:00:00Z"

    mapper = Mapper()

    project_dto = mapper.project_from_gitlab_api(project_data)

    assert isinstance(project_dto, ProjectDTO)
    assert project_dto.project_id == 1
    assert project_dto.name == "Project 1"
    assert project_dto.path == "namespace/project1"
    assert project_dto.description == "A sample project"
    assert project_dto.release == "enabled"
    assert project_dto.visibility == "public"
    assert project_dto.created_at.replace(tzinfo=None) == datetime(2024, 1, 1, 0, 0)
    assert project_dto.updated_at.replace(tzinfo=None) == datetime(2024, 1, 2, 0, 0)


def test_commit_from_gitlab_api():
    commit_data = MagicMock()
    commit_data.id = "abc123"
    commit_data.title = "Initial commit"

    commit_details = MagicMock()
    commit_details.project_id = 1
    commit_details.authored_date = "2024-01-01T00:00:00Z"
    commit_details.author_name = "John Doe"

    mapper = Mapper()

    commit_dto = mapper.commit_from_gitlab_api(commit_data, commit_details)

    assert isinstance(commit_dto, CommitDTO)
    assert commit_dto.commit_id == "abc123"
    assert commit_dto.message == "Initial commit"
    assert commit_dto.project_id == 1
    assert commit_dto.date.replace(tzinfo=None) == datetime(2024, 1, 1, 0, 0)
    assert commit_dto.author == "John Doe"
