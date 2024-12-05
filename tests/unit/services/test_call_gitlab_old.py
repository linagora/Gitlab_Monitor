# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from gitlab import exceptions as gitlab_exceptions

from gitlab_monitor.services.call_gitlab import GitlabAPIService
from gitlab_monitor.services.dto import ProjectDTO


def test_good_data_from_api_to_scan_projects():
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

    with patch("gitlab.Gitlab") as MockGitlab:
        # Configure the mock instance of GitLab
        mock_gitlab_instance = MagicMock()
        mock_gitlab_instance.projects.list.return_value = iter(mock_project_data)
        MockGitlab.return_value = mock_gitlab_instance

        mock_mapper = MagicMock()
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

        service = GitlabAPIService(
            url="https://gitlab.example.com",
            private_token="fake-token",
            mapper=mock_mapper,
        )

        result = service.scan_projects()

        assert len(result) == 2
        assert result[0].project_id == 1
        assert result[0].name == "Project 1"
        assert result[1].project_id == 2
        assert result[1].name == "Project 2"
        mock_gitlab_instance.projects.list.assert_called_once_with(iterator=True)
        mock_mapper.project_from_gitlab_api.assert_called()


def test_wrong_data_from_api_to_scan_projects():
    mock_project_data = [
        {
            "id": None,
            "name": None,
            "path_with_namespace": "namespace/project1",
            "description": "Description 1",
            "releases_access_level": "enabled",
            "visibility": "public",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-02T00:00:00Z",
        }
    ]

    with patch("gitlab.Gitlab") as MockGitlab:
        # Configure the mock instance of GitLab
        mock_gitlab_instance = MagicMock()
        mock_gitlab_instance.projects.list.return_value = iter(mock_project_data)
        MockGitlab.return_value = mock_gitlab_instance

        mock_mapper = MagicMock()

        service = GitlabAPIService(
            url="https://gitlab.example.com",
            private_token="fake-token",
            mapper=mock_mapper,
        )

        result = service.scan_projects()

        with pytest.raises(ValueError, match="Project Project 1 does not have an ID."):
            service.scan_projects()
        assert result is None
        mock_gitlab_instance.projects.list.assert_called_once_with(iterator=True)
        mock_mapper.project_from_gitlab_api.assert_not_called()
