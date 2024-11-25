# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


"""Module qui va contenir la logique métier d'appel à l'api gitlab,
project et sensé être mon DTO
"""

from gitlab_monitor.services.mapper import Mapper

import gitlab


class GitlabAPIService:
    def __init__(self, url: str, private_token: str, mapper: Mapper) -> None:
        self.gitlab_instance = gitlab.Gitlab(
            url=url,
            private_token=private_token,
            ssl_verify=False,
        )
        self._mapper = mapper

    def scan_projects(self):
        projects = self.gitlab_instance.projects.list(iterator=True)
        projects_DTO = []
        for project in projects:
            project_DTO = self._mapper.from_gitlab_api(self._mapper, project)
            projects_DTO.append(project_DTO)
        return projects_DTO