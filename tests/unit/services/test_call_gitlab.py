from unittest.mock import MagicMock
from unittest.mock import patch

import gitlab
import pytest
from gitlab import exceptions as gitlab_exceptions
from requests.exceptions import ConnectionError

from gitlab_monitor.services.call_gitlab import GitlabAPIService
from gitlab_monitor.services.dto import ProjectDTO


# === Mock return types of gitlab methods ===


class MockRESTObject:
    """Mock of a RESTObject for testing."""

    def __init__(self, data):
        self._data = data

    def __getattr__(self, item):
        return self._data.get(item, None)

    def __repr__(self):
        return f"<MockRESTObject {self._data}>"


class MockRESTObjectList:
    """Mock of a RESTObjectList for testing."""

    def __init__(self, data_list):
        self._data_list = [MockRESTObject(data) for data in data_list]

    def __iter__(self):
        return iter(self._data_list)

    def __len__(self):
        return len(self._data_list)

    def __repr__(self):
        return f"<MockRESTObjectList {self._data_list}>"


# === Fixtures ===


@pytest.fixture
def mock_gitlab():
    """Fixture to mock the gitlab instance."""
    with patch("gitlab.Gitlab") as MockGitlab:
        mock_gitlab_instance = MagicMock()
        MockGitlab.return_value = mock_gitlab_instance
        yield mock_gitlab_instance


@pytest.fixture
def gitlab_service(mock_gitlab):
    """Fixture to initialize the GitLab service."""
    return GitlabAPIService(
        url="https://gitlab.example.com",
        private_token="fake-token",
    )


# === Tests  scan_projects ===


def test_good_data_from_api_to_scan_projects(mock_gitlab, gitlab_service):
    mock_project_data = [
        {
            "id": 1,
            "name": "Project 1",
            "path_with_namespace": "namespace/project1",
            "description": "Description 1",
            "releases_access_level": "enabled",
            "visibility": "public",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-02T00:00:00Z",
        },
        {
            "id": 2,
            "name": "Project 2",
            "path_with_namespace": "namespace/project2",
            "description": "Description 2",
            "releases_access_level": "enabled",
            "visibility": "internal",
            "created_at": "2024-02-01T00:00:00Z",
            "updated_at": "2024-03-02T00:00:00Z",
        },
    ]

    mock_gitlab.projects.list.return_value = MockRESTObjectList(mock_project_data)

    result = gitlab_service.scan_projects()

    assert len(result) == 2

    mock_gitlab.projects.list.assert_called_once_with(iterator=True)


def test_scan_projects_with_invalid_url(mock_gitlab, gitlab_service, caplog):
    """Test scan_projects with bad URL, encounter a ConnectionError."""
    mock_gitlab.projects.list.side_effect = ConnectionError(
        "Unable to connect to GitLab"
    )

    with pytest.raises(SystemExit) as e:
        gitlab_service.scan_projects()
    assert e.value.code == 1

    mock_gitlab.projects.list.assert_called_once_with(iterator=True)
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert "Error when retrieving projects due to bad url:" in record.message


def test_scan_projects_with_invalid_token(mock_gitlab, gitlab_service, caplog):
    mock_gitlab.projects.list.side_effect = gitlab.exceptions.GitlabAuthenticationError(
        "Token authentification failed"
    )

    with pytest.raises(SystemExit) as e:
        gitlab_service.scan_projects()
    assert e.value.code == 1

    mock_gitlab.projects.list.assert_called_once_with(iterator=True)
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert "Authentication error due to bad token:" in record.message


def test_scan_projects_with_invalid_certificate(mock_gitlab, gitlab_service, caplog):
    mock_gitlab.projects.list.side_effect = OSError(
        "Could not find a suitable TLS CA certificate bundle, invalid path:"
    )

    with pytest.raises(SystemExit) as e:
        gitlab_service.scan_projects()
    assert e.value.code == 1

    mock_gitlab.projects.list.assert_called_once_with(iterator=True)
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert "Wrong path to gitlab authentifcation certificate:" in record.message


def test_scan_projects_with_without_certificat(mock_gitlab, gitlab_service, caplog):
    mock_project_data = [
        {
            "id": 1,
            "name": "Project 1",
            "path_with_namespace": "namespace/project1",
            "description": "Description 1",
            "releases_access_level": "enabled",
            "visibility": "public",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-02T00:00:00Z",
        },
        {
            "id": 2,
            "name": "Project 2",
            "path_with_namespace": "namespace/project2",
            "description": "Description 2",
            "releases_access_level": "enabled",
            "visibility": "internal",
            "created_at": "2024-02-01T00:00:00Z",
            "updated_at": "2024-03-02T00:00:00Z",
        },
    ]

    mock_gitlab.projects.list.return_value = MockRESTObjectList(mock_project_data)

    result = gitlab_service.scan_projects()

    assert len(result) == 2

    mock_gitlab.projects.list.assert_called_once_with(iterator=True)

    for record in caplog.records:
        assert record.levelname == "WARNING"
        assert (
            "SSL verification is not enabled. Connecting to Gitlab instance without certificate."
            in record.message
        )


# === Tests  get_project_by_id ===


def test_get_project_by_id_everything_is_good(mock_gitlab, gitlab_service):
    mock_project_data = {
        "id": 1,
        "name": "Project 1",
        "path_with_namespace": "namespace/project1",
        "description": "Description 1",
        "releases_access_level": "enabled",
        "visibility": "public",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z",
    }

    mock_gitlab.projects.get.return_value = MockRESTObject(mock_project_data)

    result = gitlab_service.get_project_by_id(1)

    assert result.id == 1
    assert result.name == "Project 1"

    mock_gitlab.projects.get.assert_called_once_with(1)


@patch("gitlab_monitor.services.call_gitlab.logger")
def test_get_project_by_id_not_found(mock_logger, mock_gitlab, gitlab_service, caplog):
    mock_gitlab.projects.get.side_effect = gitlab_exceptions.GitlabGetError(
        response_code=404, error_message="404 Project Not Found"
    )

    with pytest.raises(SystemExit) as e:
        gitlab_service.get_project_by_id(9999)
    assert e.value.code == 1

    mock_gitlab.projects.get.assert_called_once_with(9999)
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert "Error when retrieving project id 9999" in record.message


def test_get_project_by_id_bad_gitlab_url(mock_gitlab, gitlab_service, caplog):
    mock_gitlab.projects.get.side_effect = ConnectionError(
        "Unable to connect to GitLab"
    )

    with pytest.raises(SystemExit) as e:
        gitlab_service.get_project_by_id(4130)
    assert e.value.code == 1

    mock_gitlab.projects.get.assert_called_once_with(4130)
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert "Error when retrieving projects due to bad url:" in record.message


def test_get_project_by_id_with_invalid_token(mock_gitlab, gitlab_service, caplog):
    mock_gitlab.projects.get.side_effect = gitlab.exceptions.GitlabAuthenticationError(
        "Token authentification failed"
    )

    with pytest.raises(SystemExit) as e:
        gitlab_service.get_project_by_id(4130)
    assert e.value.code == 1

    mock_gitlab.projects.get.assert_called_once_with(4130)
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert "Authentication error due to bad token:" in record.message


def test_get_project_by_id_with_invalid_certificate(
    mock_gitlab, gitlab_service, caplog
):
    mock_gitlab.projects.get.side_effect = OSError(
        "Could not find a suitable TLS CA certificate bundle, invalid path:"
    )

    with pytest.raises(SystemExit) as e:
        gitlab_service.get_project_by_id(4130)
    assert e.value.code == 1

    mock_gitlab.projects.get.assert_called_once_with(4130)
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert "Wrong path to gitlab authentifcation certificate:" in record.message


def test_get_project_by_id_without_certificate(mock_gitlab, gitlab_service, caplog):
    mock_project_data = {
        "id": 1,
        "name": "Project 1",
        "path_with_namespace": "namespace/project1",
        "description": "Description 1",
        "releases_access_level": "enabled",
        "visibility": "public",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z",
    }

    mock_gitlab.projects.get.return_value = MockRESTObject(mock_project_data)

    result = gitlab_service.get_project_by_id(1)

    assert result.id == 1
    assert result.name == "Project 1"

    mock_gitlab.projects.get.assert_called_once_with(1)

    for record in caplog.records:
        assert record.levelname == "WARNING"
        assert (
            "SSL verification is not enabled. Connecting to Gitlab instance without certificate."
            in record.message
        )


# === Tests  get_project_commit ===


def test_good_data_from_api_to_get_project_commit(gitlab_service):
    commits_list = [
        {
            "id": 1,
            "title": "Commit 1",
        },
        {
            "id": 2,
            "name": "Commit 2",
        },
        {
            "id": 3,
            "name": "Commit 3",
        },
    ]
    mock_project_data = {
        "id": 1,
        "name": "Project 1",
        "path_with_namespace": "namespace/project1",
        "description": "Description 1",
        "releases_access_level": "enabled",
        "visibility": "public",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z",
    }

    mock_project = MockRESTObject(mock_project_data)

    with patch.object(mock_project, "commits") as mock_commits:
        mock_commits.list.return_value = MockRESTObjectList(commits_list)

        result = gitlab_service.get_project_commit(mock_project)

        assert len(result) == 3

        mock_commits.list.assert_called_once_with(get_all=True, all=True)
