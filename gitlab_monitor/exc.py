"""Module used to create exception raised by the gitlab_monitor codebase.
"""


class CommitNotFoundError(Exception):
    """Custom exception raised when a commit is not found in the database."""

    def __init__(self, commit_id: str):
        """
        Initialize the CommitNotFoundError with a specific commit ID.

        :param commit_id: The ID of the commit that could not be found.
        """
        self.commit_id = commit_id
        self.message = (
            f"Commit with ID '{commit_id}' was not found in the database. "
            "This error is raised by the `gitlab_monitor` codebase when a commit "
            "is expected to exist but cannot be located."
        )
        super().__init__(self.message)


class ProjectNotFoundError(Exception):
    """Custom exception raised when a project is not found in the database."""

    def __init__(self, project_id: str):
        """
        Initialize the ProjectNotFoundError with a specific project ID.

        :param project_id: The ID of the project that could not be found.
        """
        self.project_id = project_id
        self.message = (
            f"Project with ID '{project_id}' was not found in the database. "
            "This error is raised by the `gitlab_monitor` codebase when a project "
            "is expected to exist but cannot be located."
        )
        super().__init__(self.message)
