# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""Module that contains data object transfer logic for the project object from gitlab.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProjectDTO:  # pylint: disable=too-many-instance-attributes
    """This is a data transfer object, used to store information
    in memory to serialize data more easily.
    It adds an additional layer of abstraction to better
    decouple the code before storing it in the database."""

    project_id: int
    name: str
    path: str
    description: str
    release: str
    visibility: str
    created_at: datetime
    updated_at: datetime


@dataclass
class CommitDTO:
    """This is a data transfer object, used to store information
    in memory to serialize data more easily.
    It adds an additional layer of abstraction to better
    decouple the code before storing it in the database."""

    commit_id: str
    project_id: int
    message: str
    date: datetime
    author: str
