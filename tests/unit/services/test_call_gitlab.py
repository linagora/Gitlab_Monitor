from unittest.mock import Mock

import pytest

from gitlab_monitor.services.call_gitlab import GitlabAPIService
from gitlab_monitor.services.mapper import Mapper

@pytest.fixture
def gitlab_service():
    mapper = Mock(Mapper)
    return GitlabAPIService(
        url="https://ci.linagora.com",
        private_token="fake_token",
        mapper=mapper,
        ssl_cert_path=None
    )

def test_scan_projects_with_mock(gitlab_service):
    # Prepare the mock projects to simulate the GitLab API response.
    mock_projects = [{
        'id': 1,
        'name': 'Project 1',
        'path_with_namespace': 'namespace/project1',
        'description': 'Description 1',
        'releases_access_level': 'enabled',
        'visibility': 'public',
        'created_at': '2024-01-01T00:00:00Z',
        'updated_at': '2024-01-02T00:00:00Z'
    }]

    gitlab_service._mapper.from_gitlab_api.return_value = "project_dto"

    # Call my function with mock projects (an optional parameter).
    response = gitlab_service.scan_projects(mock_projects=mock_projects)

    # Checks that the rest of my function has behaved appropriately.
    assert len(response) == 1
    assert response[0] == "project_dto"
    gitlab_service._mapper.from_gitlab_api.assert_called_once()