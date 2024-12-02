
# # --- Copyright (c) 2024 Linagora
# # licence       : GNU GENERAL PUBLIC LICENSE
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from dataclasses import dataclass


@dataclass
class ProjectDTO:
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
    created_at: str
    updated_at: str