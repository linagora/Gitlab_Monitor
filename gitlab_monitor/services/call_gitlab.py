
# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com










"""Module qui va contenir la logique métier d'appel à l'api gitlab,
project et sensé être mon DTO
"""

import gitlab
from mapper import Mapper


class GitlabAPIService:
    def __init__(self, url: str, private_token: str, mapper: Mapper) -> None:
        self._gl_test = gitlab.Gitlab(
            url=url,
            private_token=private_token,
            ssl_verify=False,
        )
        self._mapper = mapper

    def scan_projects(self):
        api_response = self._gl_test.projects.list(get_all=True)
        projects = []
        for project_data in api_response:
            project_dto = self._mapper.from_gitlab_api(project_data)
            projects.append(project_dto)
        return projects
