import gitlab
import pytest
from unittest.mock import MagicMock, patch
from gitlab import exceptions as gitlab_exceptions
from requests.exceptions import ConnectionError

from gitlab_monitor.services.call_gitlab import GitlabAPIService
from gitlab_monitor.services.dto import ProjectDTO


# === Fixtures ===

@pytest.fixture
def mock_gitlab():
    """Fixture pour mocker l'instance GitLab."""
    with patch("gitlab.Gitlab") as MockGitlab:
        mock_gitlab_instance = MagicMock()
        MockGitlab.return_value = mock_gitlab_instance
        yield mock_gitlab_instance


@pytest.fixture
def mock_mapper():
    """Fixture pour mocker le mapper."""
    return MagicMock()


@pytest.fixture
def gitlab_service(mock_gitlab, mock_mapper):
    """Fixture pour initialiser le service GitLab."""
    return GitlabAPIService(
        url="https://gitlab.example.com",
        private_token="fake-token",
        mapper=mock_mapper,
    )


# === Tests  scan_projects ===

def test_good_data_from_api_to_scan_projects(mock_gitlab, mock_mapper, gitlab_service):
    mock_project_data = [
        {
            'id': 1,
            'name': 'Project 1',
            'path_with_namespace': 'namespace/project1',
            'description': 'Description 1',
            'releases_access_level': 'enabled',
            'visibility': 'public',
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-02T00:00:00Z',
        },
        {
            'id': 2,
            'name': 'Project 2',
            'path_with_namespace': 'namespace/project2',
            'description': 'Description 2',
            'releases_access_level': 'enabled',
            'visibility': 'internal',
            'created_at': '2024-02-01T00:00:00Z',
            'updated_at': '2024-03-02T00:00:00Z',
        },
    ]

    mock_gitlab.projects.list.return_value = iter(mock_project_data)

    mock_mapper.project_from_gitlab_api.side_effect = [
        ProjectDTO(
            project_id=project["id"],
            name=project["name"],
            path=project["path_with_namespace"],
            description=project["description"],
            release=project["releases_access_level"],
            visibility=project["visibility"],
            created_at=project["created_at"],
            updated_at=project["updated_at"],
        )
        for project in mock_project_data
    ]

    result = gitlab_service.scan_projects()

    assert len(result) == 2
    assert result[0].project_id == 1
    assert result[0].name == "Project 1"
    assert result[1].project_id == 2
    assert result[1].name == "Project 2"
    mock_gitlab.projects.list.assert_called_once_with(iterator=True)
    mock_mapper.project_from_gitlab_api.assert_called()


def test_scan_projects_with_invalid_url(mock_gitlab, gitlab_service, caplog):
    """Test scan_projects avec une URL incorrecte provoquant une ConnectionError."""
    mock_gitlab.projects.list.side_effect = ConnectionError("Unable to connect to GitLab")

    # TODO: accorder au sys.exit(1) dans le code & exception est attrapée pas levée.
    with pytest.raises(ConnectionError, match="Unable to connect to GitLab"):
        gitlab_service.scan_projects()

    mock_gitlab.projects.list.assert_called_once_with(iterator=True)
    for record in caplog.records:
        assert record.levelname == 'ERROR'
        assert "Error when retrieving projects due to bad url:" in record.message


def test_scan_projects_with_invalid_token(mock_gitlab, gitlab_service, caplog):
    mock_gitlab.projects.list.side_effect = gitlab.exceptions.GitlabAuthenticationError("Token authentification failed")

    with pytest.raises(gitlab.exceptions.GitlabAuthenticationError, match="Token authentification failed"):
        gitlab_service.scan_projects()

    mock_gitlab.projects.list.assert_called_once_with(iterator=True)
    for record in caplog.records:
        assert record.levelname == 'ERROR'
        assert "Authentication error due to bad token:" in record.message

def test_scan_projects_with_invalid_certificate(mock_gitlab, gitlab_service, caplog):
    mock_gitlab.projects.list.side_effect = OSError("Could not find a suitable TLS CA certificate bundle, invalid path:")

    with pytest.raises(OSError, match="Could not find a suitable TLS CA certificate bundle, invalid path:"):
        gitlab_service.scan_projects()

    mock_gitlab.projects.list.assert_called_once_with(iterator=True)
    for record in caplog.records:
        assert record.levelname == 'ERROR'
        assert "Wrong path to gitlab authentifcation certificate:" in record.message

def test_scan_projects_with_without_certificat(mock_gitlab, gitlab_service, caplog, mock_mapper):
    mock_project_data = [
        {
            'id': 1,
            'name': 'Project 1',
            'path_with_namespace': 'namespace/project1',
            'description': 'Description 1',
            'releases_access_level': 'enabled',
            'visibility': 'public',
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-02T00:00:00Z',
        },
        {
            'id': 2,
            'name': 'Project 2',
            'path_with_namespace': 'namespace/project2',
            'description': 'Description 2',
            'releases_access_level': 'enabled',
            'visibility': 'internal',
            'created_at': '2024-02-01T00:00:00Z',
            'updated_at': '2024-03-02T00:00:00Z',
        },
    ]

    mock_gitlab.projects.list.return_value = iter(mock_project_data)

    mock_mapper.project_from_gitlab_api.side_effect = [
        ProjectDTO(
            project_id=project["id"],
            name=project["name"],
            path=project["path_with_namespace"],
            description=project["description"],
            release=project["releases_access_level"],
            visibility=project["visibility"],
            created_at=project["created_at"],
            updated_at=project["updated_at"],
        )
        for project in mock_project_data
    ]

    result = gitlab_service.scan_projects()

    assert len(result) == 2
    assert result[0].project_id == 1
    assert result[0].name == "Project 1"
    assert result[1].project_id == 2
    assert result[1].name == "Project 2"
    mock_gitlab.projects.list.assert_called_once_with(iterator=True)
    mock_mapper.project_from_gitlab_api.assert_called()

    for record in caplog.records:
        assert record.levelname == 'WARNING'
        assert "SSL verification is not enabled. Connecting to Gitlab instance without certificate." in record.message


# === Tests  get_project_by_id ===

def test_get_project_by_id_everything_is_good(mock_gitlab, mock_mapper, gitlab_service):
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

    mock_gitlab.projects.get.return_value = mock_project_data

    mock_mapper.project_from_gitlab_api.return_value = ProjectDTO(
        project_id=mock_project_data["id"],
        name=mock_project_data["name"],
        path=mock_project_data["path_with_namespace"],
        description=mock_project_data["description"],
        release=mock_project_data["releases_access_level"],
        visibility=mock_project_data["visibility"],
        created_at=mock_project_data["created_at"],
        updated_at=mock_project_data["updated_at"],
    )

    result = gitlab_service.get_project_by_id(1)

    assert result.project_id == 1
    assert result.name == "Project 1"
    mock_gitlab.projects.get.assert_called_once_with(1)
    mock_mapper.project_from_gitlab_api.assert_called()


@patch('gitlab_monitor.services.call_gitlab.logger')
def test_get_project_by_id_not_found(mock_logger, mock_gitlab, gitlab_service, caplog):
    mock_gitlab.projects.get.side_effect = gitlab_exceptions.GitlabGetError(
        response_code=404, error_message="404 Project Not Found"
    )

    with pytest.raises(gitlab_exceptions.GitlabGetError, match="404 Project Not Found"):
        gitlab_service.get_project_by_id(9999)

    mock_gitlab.projects.get.assert_called_once_with(9999)
    for record in caplog.records:
        assert record.levelname == 'ERROR'
        assert "Error when retrieving project id 9999" in record.message


def test_get_project_by_id_bad_gitlab_url(mock_gitlab, gitlab_service, caplog):
    mock_gitlab.projects.list.side_effect = ConnectionError("Unable to connect to GitLab")

    with pytest.raises(ConnectionError, match="Unable to connect to GitLab"):
        gitlab_service.get_project_by_id(4130)

    mock_gitlab.projects.get.assert_called_once_with(4130)
    for record in caplog.records:
        assert record.levelname == 'ERROR'
        assert "Error when retrieving projects due to bad url:" in record.message


def test_get_project_by_id_with_invalid_token(mock_gitlab, gitlab_service, caplog):
    mock_gitlab.projects.list.side_effect = gitlab.exceptions.GitlabAuthenticationError("Token authentification failed")

    with pytest.raises(gitlab.exceptions.GitlabAuthenticationError, match="Token authentification failed"):
        gitlab_service.get_project_by_id(4130)

    mock_gitlab.projects.get.assert_called_once_with(4130)
    for record in caplog.records:
        assert record.levelname == 'ERROR'
        assert "Authentication error due to bad token:" in record.message

def test_get_project_by_id_with_invalid_certificate(mock_gitlab, gitlab_service, caplog):
    mock_gitlab.projects.list.side_effect = OSError("Could not find a suitable TLS CA certificate bundle, invalid path:")

    with pytest.raises(OSError, match="Could not find a suitable TLS CA certificate bundle, invalid path:"):
        gitlab_service.get_project_by_id(4130)

    mock_gitlab.projects.get.assert_called_once_with(4130)
    for record in caplog.records:
        assert record.levelname == 'ERROR'
        assert "Wrong path to gitlab authentifcation certificate:" in record.message


def test_get_project_by_id_without_certificate(mock_gitlab, mock_mapper, gitlab_service, caplog):
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

    mock_gitlab.projects.get.return_value = mock_project_data

    mock_mapper.project_from_gitlab_api.return_value = ProjectDTO(
        project_id=mock_project_data["id"],
        name=mock_project_data["name"],
        path=mock_project_data["path_with_namespace"],
        description=mock_project_data["description"],
        release=mock_project_data["releases_access_level"],
        visibility=mock_project_data["visibility"],
        created_at=mock_project_data["created_at"],
        updated_at=mock_project_data["updated_at"],
    )

    result = gitlab_service.get_project_by_id(1)

    assert result.project_id == 1
    assert result.name == "Project 1"
    mock_gitlab.projects.get.assert_called_once_with(1)
    mock_mapper.project_from_gitlab_api.assert_called()

    for record in caplog.records:
        assert record.levelname == 'WARNING'
        assert "SSL verification is not enabled. Connecting to Gitlab instance without certificate." in record.message