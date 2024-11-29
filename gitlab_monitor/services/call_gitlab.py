# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


"""Module qui va contenir la logique métier d'appel à l'api gitlab,
project et sensé être mon DTO
"""

from typing import Optional

import gitlab

from gitlab_monitor.services.mapper import Mapper


class GitlabAPIService:
    def __init__(
        self,
        url: str,
        private_token: str,
        mapper: Mapper,
        ssl_cert_path: Optional[str] = None,
    ) -> None:
        self.gitlab_instance = gitlab.Gitlab(
            url=url,
            private_token=private_token,
            ssl_verify=ssl_cert_path if ssl_cert_path else True,
        )
        self._mapper = mapper

    def scan_projects(self):
        print("Retrieving projects...")
        projects = self.gitlab_instance.projects.list(iterator=True)
        projects_DTO = []
        for project in projects:
            project_DTO = self._mapper.from_gitlab_api(self._mapper, project)
            projects_DTO.append(project_DTO)
        return projects_DTO

    def get_project_by_id(self, project_id):
        print(f"Retrieving project id {project_id}...")
        try:
            project = self.gitlab_instance.projects.get(project_id)
            return self._mapper.from_gitlab_api(self._mapper, project)
        except Exception as e:
            print(f"Error when retrieving project id {project_id}: {e}")
            return None
