
# # --- Copyright (c) 2024 Linagora
# # licence       : GNU GENERAL PUBLIC LICENSE
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

from io import StringIO
import sys
from unittest.mock import MagicMock, patch
from gitlab import exceptions as gitlab_exceptions


from gitlab_monitor.services.call_gitlab import GitlabAPIService
from gitlab_monitor.services.dto import ProjectDTO


def test_scan_projects():
    # Prepare the mock response for the GitLab API response
    mock_project_data = [{
        'id': 1,
        'name': 'Project 1',
        'path_with_namespace': 'namespace/project1',
        'description': 'Description 1',
        'releases_access_level': 'enabled',
        'visibility': 'public',
        'created_at': '2024-01-01T00:00:00Z',
        'updated_at': '2024-01-02T00:00:00Z'
        }, {
        'id': 2,
        'name': 'Project 2',
        'path_with_namespace': 'namespace/project2',
        'description': 'Description 2',
        'releases_access_level': 'enabled',
        'visibility': 'internal',
        'created_at': '2024-02-01T00:00:00Z',
        'updated_at': '2024-03-02T00:00:00Z'
        }]
        
    # Mock the gitlab.Gitlab class
    with patch("gitlab.Gitlab") as MockGitlab:
        # Configure the mock instance of GitLab
        mock_gitlab_instance = MagicMock()
        mock_gitlab_instance.projects.list.return_value = iter(mock_project_data)
        MockGitlab.return_value = mock_gitlab_instance

         # Mock mapper
        mock_mapper = MagicMock()
        mock_mapper.from_gitlab_api.side_effect = [
            ProjectDTO(
                project_id=project['id'],
                name=project['name'],
                path=project['path_with_namespace'],
                description=project['description'],
                release=project['releases_access_level'],
                visibility=project['visibility'],
                created_at=project['created_at'],
                updated_at=project['updated_at']
            ) for project in mock_project_data
        ]

        # Create the service with the mock mapper
        service = GitlabAPIService(
            url="https://gitlab.example.com",
            private_token="fake-token",
            mapper=mock_mapper,
        )

        # Call the service with the mock projects
        result = service.scan_projects()

        # Assertions
        assert len(result) == 2
        assert result[0].project_id == 1
        assert result[0].name == 'Project 1'
        assert result[1].project_id == 2
        assert result[1].name == 'Project 2'
        mock_gitlab_instance.projects.list.assert_called_once_with(iterator=True)
        mock_mapper.from_gitlab_api.assert_called()

def test_get_project_by_id():
    mock_project_data = {
        'id': 1,
        'name': 'Project 1',
        'path_with_namespace': 'namespace/project1',
        'description': 'Description 1',
        'releases_access_level': 'enabled',
        'visibility': 'public',
        'created_at': '2024-01-01T00:00:00Z',
        'updated_at': '2024-01-02T00:00:00Z'
        }
        
    with patch("gitlab.Gitlab") as MockGitlab:
        mock_gitlab_instance = MagicMock()
        MockGitlab.return_value = mock_gitlab_instance

        mock_mapper = MagicMock()
        mock_mapper.from_gitlab_api.return_value = ProjectDTO(
                project_id=mock_project_data['id'],
                name=mock_project_data['name'],
                path=mock_project_data['path_with_namespace'],
                description=mock_project_data['description'],
                release=mock_project_data['releases_access_level'],
                visibility=mock_project_data['visibility'],
                created_at=mock_project_data['created_at'],
                updated_at=mock_project_data['updated_at']
            )

        service = GitlabAPIService(
            url="https://gitlab.example.com",
            private_token="fake-token",
            mapper=mock_mapper,
        )

        result = service.get_project_by_id(1)

        assert result.project_id == 1
        assert result.name == 'Project 1'
        mock_gitlab_instance.projects.get.assert_called_once_with(1)
        mock_mapper.from_gitlab_api.assert_called()

def test_get_project_by_id_not_found():
    with patch("gitlab.Gitlab") as MockGitlab:
        mock_gitlab_instance = MagicMock()
        mock_gitlab_instance.projects.get.side_effect = gitlab_exceptions.GitlabGetError(
            response_code=404, error_message="404 Project Not Found"
        )
        MockGitlab.return_value = mock_gitlab_instance
        mock_mapper = MagicMock()

        service = GitlabAPIService(
            url="https://gitlab.example.com",
            private_token="fake-token",
            mapper=mock_mapper,
        )

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Call the method to test
        result = service.get_project_by_id(9999)

        # Reset redirect.
        sys.stdout = sys.__stdout__

        # Assertions
        assert result is None
        assert "Error when retrieving project id 9999: 404: 404 Project Not Found" in captured_output.getvalue()
        mock_gitlab_instance.projects.get.assert_called_once_with(9999)        