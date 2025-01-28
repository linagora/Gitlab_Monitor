# # --- Copyright (c) 2024-2025 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com
import json
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import call
from unittest.mock import mock_open
from unittest.mock import patch

import pytest

from gitlab_monitor.controller.controller import ArchiveProjectCommand
from gitlab_monitor.controller.controller import GetProjectCommand
from gitlab_monitor.controller.controller import GetProjectsCommand
from gitlab_monitor.logger.logger import logger
from gitlab_monitor.services.dto import CommitDTO
from gitlab_monitor.services.dto import ProjectDTO
from gitlab_monitor.services.mapper import Mapper
from gitlab_monitor.services.pretty_print import PrintCommitDTO
from gitlab_monitor.services.pretty_print import PrintProjectDTO


# === Fixtures ===


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Set required environment variables for tests."""
    monkeypatch.setenv("GITLAB_PRIVATE_TOKEN", "mocked_token")
    monkeypatch.setenv("SSL_CERT_PATH", "/mocked/path/to/cert")
    monkeypatch.setenv("GITLAB_URL", "https://mockgitlab.com")


@pytest.fixture
def gitlab_service():
    return MagicMock()


@pytest.fixture
def project_repository():
    return MagicMock()


@pytest.fixture
def commit_repository():
    return MagicMock()


@pytest.fixture
def db():
    with patch("gitlab_monitor.controller.controller.Database") as MockDatabase:
        mock_db = MockDatabase.return_value
        mock_db._initialize_database = MagicMock()
        mock_db._session = MagicMock()
        yield mock_db


@pytest.fixture
def get_projects_command(gitlab_service, project_repository, db):
    command = GetProjectsCommand(kwargs={"no_db": False})
    command.gitlab_service = gitlab_service
    command.project_repository = project_repository
    command._no_db = False
    command.db = db
    return command


@pytest.fixture
def get_project_command(gitlab_service, project_repository, db):
    command = GetProjectCommand(kwargs={"no_db": False})
    command.gitlab_service = gitlab_service
    command.project_repository = project_repository
    command._no_db = False
    command.db = db
    return command


@pytest.fixture
def archive_project_command(gitlab_service, project_repository, db):
    command = ArchiveProjectCommand(kwargs={"no_db": False})
    command.gitlab_service = gitlab_service
    command.project_repository = project_repository
    command._no_db = False
    command.db = db
    return command


# === Tests  GetProjectsCommand execute ===


def test_get_projects_command_execute_no_options(get_projects_command):
    projects = [
        MagicMock(),
        MagicMock(),
    ]
    projects_dto = [
        ProjectDTO(
            project_id=1,
            name="Project 1",
            path="namespace/project1",
            description="Description 1",
            release="enabled",
            visibility="public",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-02T00:00:00Z",
        ),
        ProjectDTO(
            project_id=2,
            name="Project 2",
            path="namespace/project2",
            description="Description 2",
            release="enabled",
            visibility="internal",
            created_at="2024-02-01T00:00:00Z",
            updated_at="2024-03-02T00:00:00Z",
        ),
    ]
    get_projects_command.global_options = MagicMock()
    get_projects_command._save_projects = MagicMock()

    get_projects_command.gitlab_service.scan_projects.return_value = projects

    with patch.object(Mapper, "project_from_gitlab_api", side_effect=projects_dto):
        kwargs = {"no_db": False}
        get_projects_command.execute(kwargs)

        get_projects_command.gitlab_service.scan_projects.assert_called_once()
        assert Mapper().project_from_gitlab_api.call_count == 2
        get_projects_command._save_projects.assert_called_once_with(projects_dto)


def test_get_projects_command_execute_with_no_database_options(get_projects_command):
    projects = [
        MagicMock(),
        MagicMock(),
    ]
    projects_dto = [
        ProjectDTO(
            project_id=1,
            name="Project 1",
            path="namespace/project1",
            description="Description 1",
            release="enabled",
            visibility="public",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-02T00:00:00Z",
        ),
        ProjectDTO(
            project_id=2,
            name="Project 2",
            path="namespace/project2",
            description="Description 2",
            release="enabled",
            visibility="internal",
            created_at="2024-02-01T00:00:00Z",
            updated_at="2024-03-02T00:00:00Z",
        ),
    ]
    get_projects_command.global_options = MagicMock()
    get_projects_command._save_projects = MagicMock()

    get_projects_command.gitlab_service.scan_projects.return_value = projects

    with patch.object(
        PrintProjectDTO, "print_dto_list", MagicMock()
    ) as mock_print_dto_list:
        with patch.object(Mapper, "project_from_gitlab_api", side_effect=projects_dto):
            kwargs = {"no_db": True}
            get_projects_command._no_db = True
            get_projects_command.execute(kwargs)

            get_projects_command.gitlab_service.scan_projects.assert_called_once()
            assert Mapper().project_from_gitlab_api.call_count == 2
            mock_print_dto_list.assert_called_once_with(projects_dto, "Projects")
            get_projects_command._save_projects.assert_not_called()


def test_get_projects_command_execute_with_unused_since_options(get_projects_command):
    projects = [
        MagicMock(),
        MagicMock(),
    ]
    projects[0].updated_at = "2024-02-02T00:00:00Z"
    projects[1].updated_at = "2024-04-02T00:00:00Z"
    projects_dto = [
        ProjectDTO(
            project_id=1,
            name="Project 1",
            path="namespace/project1",
            description="Description 1",
            release="enabled",
            visibility="public",
            created_at=datetime.fromisoformat("2024-01-01T00:00:00Z"),
            updated_at=datetime.fromisoformat("2024-02-02T00:00:00Z"),
        ),
        ProjectDTO(
            project_id=2,
            name="Project 2",
            path="namespace/project2",
            description="Description 2",
            release="enabled",
            visibility="internal",
            created_at=datetime.fromisoformat("2024-02-01T00:00:00Z"),
            updated_at=datetime.fromisoformat("2024-04-02T00:00:00Z"),
        ),
    ]
    get_projects_command.global_options = MagicMock()
    get_projects_command._save_projects = MagicMock()

    get_projects_command.gitlab_service.scan_projects.return_value = projects

    with patch.object(Mapper, "project_from_gitlab_api", side_effect=projects_dto):
        unused_since_datetime = datetime.fromisoformat("2024-03-01T00:00:00Z").replace(
            tzinfo=None
        )
        kwargs = {"unused_since": unused_since_datetime}
        get_projects_command._no_db = False
        get_projects_command._unused_since = unused_since_datetime
        get_projects_command.execute(kwargs)

        get_projects_command.gitlab_service.scan_projects.assert_called_once()
        assert Mapper().project_from_gitlab_api.call_count == 1
        get_projects_command._save_projects.assert_called_once_with([projects_dto[0]])


def test_get_projects_command_execute_with_option_save_in_file(
    get_projects_command, caplog
):
    projects = [
        MagicMock(),
        MagicMock(),
    ]
    projects_dto = [
        ProjectDTO(
            project_id=1,
            name="Project 1",
            path="namespace/project1",
            description="Description 1",
            release="enabled",
            visibility="public",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-02T00:00:00Z",
        ),
        ProjectDTO(
            project_id=2,
            name="Project 2",
            path="namespace/project2",
            description="Description 2",
            release="enabled",
            visibility="internal",
            created_at="2024-02-01T00:00:00Z",
            updated_at="2024-03-02T00:00:00Z",
        ),
    ]
    get_projects_command.global_options = MagicMock()
    get_projects_command._save_projects = MagicMock()
    get_projects_command.gitlab_service.scan_projects.return_value = projects

    with patch("builtins.open", MagicMock()) as mock_open:

        with patch.object(Mapper, "project_from_gitlab_api", side_effect=projects_dto):
            kwargs = {"save_in_file": "test-file"}
            get_projects_command._save_in_file = kwargs["save_in_file"]
            get_projects_command.execute(kwargs)

            mock_open.assert_called_once_with(
                "saved_datas/projects/test-file.json", "w", encoding="utf-8"
            )

        for record in caplog.records:
            assert record.levelname == "INFO"
            assert (
                "%s Projects have been retrieved and saved in the file saved_datas/projects/%s.json.",
                len(projects_dto),
                "test-file",
            ) in record.message

            get_projects_command.gitlab_service.scan_projects.assert_called_once()
            assert Mapper().project_from_gitlab_api.call_count == 2
            get_projects_command._save_projects.assert_not_called()


# === Tests  GetProjectsCommand _save_projects ===


def test_save_projects(get_projects_command, caplog):
    projects_dto = [
        ProjectDTO(
            project_id=1,
            name="Project 1",
            path="namespace/project1",
            description="Description 1",
            release="enabled",
            visibility="public",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-02T00:00:00Z",
        ),
        ProjectDTO(
            project_id=2,
            name="Project 2",
            path="namespace/project2",
            description="Description 2",
            release="enabled",
            visibility="internal",
            created_at="2024-02-01T00:00:00Z",
            updated_at="2024-03-02T00:00:00Z",
        ),
    ]
    get_projects_command.project_repository.create = MagicMock()

    get_projects_command._save_projects(projects_dto)

    assert get_projects_command.project_repository.create.call_count == 2

    for record in caplog.records:
        assert record.levelname == "INFO"
        assert (
            "%d projects have been retrieved and saved or updated in the database.",
            len(projects_dto),
        ) in record.message


# === Tests  GetProjectCommand execute ===


def test_get_project_command_execute_no_options(get_project_command):
    project = MagicMock()
    dto_project = ProjectDTO(
        project_id=1,
        name="Project 1",
        path="namespace/project1",
        description="Description 1",
        release="enabled",
        visibility="public",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-02T00:00:00Z",
    )

    get_project_command.global_options = MagicMock()
    get_project_command._save_project = MagicMock()

    get_project_command.gitlab_service.get_project_by_id.return_value = project

    with patch.object(Mapper, "project_from_gitlab_api", return_value=dto_project):
        kwargs = {"id": 1, "get_commits": False, "no_db": False}

        get_project_command.execute(kwargs)

        get_project_command.gitlab_service.get_project_by_id.assert_called_once_with(1)
        Mapper().project_from_gitlab_api.assert_called_once_with(project)
        get_project_command._save_project.assert_called_once_with(dto_project)


def test_get_project_command_execute_with_no_database_option(get_project_command):
    project = MagicMock()
    dto_project = ProjectDTO(
        project_id=1,
        name="Project 1",
        path="namespace/project1",
        description="Description 1",
        release="enabled",
        visibility="public",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-02T00:00:00Z",
    )

    get_project_command.global_options = MagicMock()
    get_project_command._save_project = MagicMock()

    get_project_command.gitlab_service.get_project_by_id.return_value = project

    with patch.object(PrintProjectDTO, "print_dto", MagicMock()) as mock_print_dto:
        with patch.object(Mapper, "project_from_gitlab_api", return_value=dto_project):
            kwargs = {"id": 1, "get_commits": False, "no_db": True}
            get_project_command._no_db = True

            get_project_command.execute(kwargs)

            get_project_command.gitlab_service.get_project_by_id.assert_called_once_with(
                1
            )
            Mapper().project_from_gitlab_api.assert_called_once_with(project)
            get_project_command._save_project.assert_not_called()
            mock_print_dto.assert_called_once_with(dto_project)


def test_get_project_command_execute_with_commit_option(get_project_command):
    project = MagicMock()
    dto_project = ProjectDTO(
        project_id=1,
        name="Project 1",
        path="namespace/project1",
        description="Description 1",
        release="enabled",
        visibility="public",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-02T00:00:00Z",
    )

    get_project_command.global_options = MagicMock()
    get_project_command._save_project = MagicMock()
    get_project_command._get_commits = MagicMock()

    get_project_command.gitlab_service.get_project_by_id.return_value = project

    with patch.object(Mapper, "project_from_gitlab_api", return_value=dto_project):
        kwargs = {"id": 1, "get_commits": True, "no_db": False}

        get_project_command.execute(kwargs)

        get_project_command.gitlab_service.get_project_by_id.assert_called_once_with(1)
        Mapper().project_from_gitlab_api.assert_called_once_with(project)
        get_project_command._save_project.assert_called_once_with(dto_project)
        get_project_command._get_commits.assert_called_once_with(project)


def test_get_project_command_execute_with_option_save_in_file(
    get_project_command, caplog
):
    project = MagicMock()
    dto_project = ProjectDTO(
        project_id=1,
        name="Project 1",
        path="namespace/project1",
        description="Description 1",
        release="enabled",
        visibility="public",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-02T00:00:00Z",
    )

    get_project_command.global_options = MagicMock()
    get_project_command._save_project = MagicMock()
    get_project_command.gitlab_service.get_project_by_id.return_value = project

    with patch("builtins.open", MagicMock()) as mock_open, patch.object(
        Mapper, "project_from_gitlab_api", return_value=dto_project
    ):

        kwargs = {
            "id": 1,
            "get_commits": False,
            "no_db": False,
            "save_in_file": "test-file",
        }
        get_project_command._save_in_file = kwargs["save_in_file"]

        get_project_command.execute(kwargs)

        get_project_command.gitlab_service.get_project_by_id.assert_called_once_with(1)
        Mapper().project_from_gitlab_api.assert_called_once_with(project)
        get_project_command._save_project.assert_not_called()

        mock_open.assert_called_once_with(
            "saved_datas/projects/test-file.json", "w", encoding="utf-8"
        )
        for record in caplog.records:
            assert record.levelname == "INFO"
            assert (
                (
                    "Project with id %d has been retrieved and saved \
                    in the file saved_datas/projects/%s.json.",
                    1,
                    "test-file",
                )
                in record.message
            )


# === Tests  GetProjectCommand _save_project ===


def test_save_project(get_project_command, caplog):
    project_dto = ProjectDTO(
        project_id=1,
        name="Project 1",
        path="namespace/project1",
        description="Description 1",
        release="enabled",
        visibility="public",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-02T00:00:00Z",
    )

    get_project_command.project_repository.create = MagicMock()

    get_project_command._save_project(project_dto)

    get_project_command.project_repository.create.assert_called_once_with(project_dto)

    for record in caplog.records:
        assert record.levelname == "INFO"
        assert (
            "Project %s has been retrieved and saved or updated in the database.",
            project_dto.name,
        ) in record.message


# === Tests  GetProjectCommand _get_commits ===


def test_get_commits(get_project_command):
    project_id = 1
    project = MagicMock()
    commits = [
        MagicMock(),
        MagicMock(),
    ]
    commits_dto = [
        CommitDTO(
            commit_id=1,
            message="Commit 1",
            project_id=project_id,
            date="2021-01-01",
            author="Test Author",
        ),
        CommitDTO(
            commit_id=2,
            message="Commit 2",
            project_id=project_id,
            date="2021-01-01",
            author="Test Author",
        ),
    ]

    get_project_command._save_commits = MagicMock()
    get_project_command.gitlab_service.get_project_commit.return_value = commits

    with patch.object(Mapper, "commit_from_gitlab_api", side_effect=commits_dto):
        get_project_command._get_commits(project)

        get_project_command.gitlab_service.get_project_commit.assert_called_once_with(
            project
        )
        assert Mapper().commit_from_gitlab_api.call_count == 2
        get_project_command._save_commits.assert_called_once_with(commits_dto, project)


def test_get_commits_no_database(get_project_command):
    project_id = 1
    project = MagicMock()
    commits = [
        MagicMock(),
        MagicMock(),
    ]
    commits_dto = [
        CommitDTO(
            commit_id=1,
            message="Commit 1",
            project_id=project_id,
            date="2021-01-01",
            author="Test Author",
        ),
        CommitDTO(
            commit_id=2,
            message="Commit 2",
            project_id=project_id,
            date="2021-01-01",
            author="Test Author",
        ),
    ]

    get_project_command._save_commits = MagicMock()
    get_project_command.gitlab_service.get_project_commit.return_value = commits

    with patch.object(
        PrintCommitDTO, "print_dto_list", MagicMock()
    ) as mock_print_dto_list:
        with patch.object(Mapper, "commit_from_gitlab_api", side_effect=commits_dto):
            get_project_command._no_db = True
            get_project_command._get_commits(project)

            get_project_command.gitlab_service.get_project_commit.assert_called_once_with(
                project
            )
            assert Mapper().commit_from_gitlab_api.call_count == 2
            get_project_command._save_commits.assert_not_called()
            mock_print_dto_list.assert_called_once_with(commits_dto, "Commits")


# === Tests  GetProjectCommand _get_commits ===


def test_save_commits(get_project_command, caplog):
    commits_dto = [
        CommitDTO(
            commit_id=1,
            message="Commit 1",
            project_id=1,
            date="2021-01-01",
            author="Test Author",
        ),
        CommitDTO(
            commit_id=2,
            message="Commit 2",
            project_id=1,
            date="2021-01-01",
            author="Test Author",
        ),
    ]

    project = MagicMock()

    get_project_command.commit_repository.create = MagicMock()

    get_project_command._save_commits(commits_dto, project)

    assert get_project_command.commit_repository.create.call_count == 2

    with patch.object(project, "name") as mock_project_name:
        for record in caplog.records:
            assert record.levelname == "INFO"
            assert (
                '%d commits from project "%s" have been retrieved and saved or updated in the database.',
                len(commits_dto),
                mock_project_name,
            ) in record.message


# === Tests ArchiveProjectCommand execute ===


def test_archive_project_by_id(archive_project_command):
    project_id = "123"
    project_mock = MagicMock()

    archive_project_command.gitlab_service.get_project_by_id.return_value = project_mock

    archive_project_command.execute({"project": project_id})

    archive_project_command.gitlab_service.get_project_by_id.assert_called_once_with(
        project_id
    )
    archive_project_command.gitlab_service.archive_project.assert_called_once_with(
        project_mock
    )


def test_archive_projects_from_json_file(archive_project_command):
    projects = [{"project_id": "123"}, {"project_id": "456"}]
    project_mocks = [MagicMock(), MagicMock()]

    archive_project_command.gitlab_service.get_project_by_id.side_effect = project_mocks

    with patch("builtins.open", mock_open(read_data=json.dumps(projects))):
        archive_project_command.execute({"project": "projects.json"})

    expected_calls = [call(project["project_id"]) for project in projects]
    archive_project_command.gitlab_service.get_project_by_id.assert_has_calls(
        expected_calls
    )
    assert archive_project_command.gitlab_service.get_project_by_id.call_count == len(
        projects
    )
    assert archive_project_command.gitlab_service.archive_project.call_count == len(
        projects
    )
