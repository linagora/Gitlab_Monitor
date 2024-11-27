# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

import os

from gitlab_monitor.services.bdd.bdd import Database
from gitlab_monitor.services.call_gitlab import GitlabAPIService
from gitlab_monitor.services.mapper import Mapper
from gitlab_monitor.services.bdd.repository import SQLAlchemyProjectRepository

from dependency_injector import containers, providers
from dotenv import load_dotenv


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    load_dotenv()
    config.private_token.from_env("GITLAB_PRIVATE_TOKEN")
    config.gitlab_url.from_value("https://ci.linagora.com")

    database = providers.Singleton(Database)
    database()._initialize_database()

    mapper = providers.Singleton(Mapper)

    gitlab_service = providers.Singleton(
        GitlabAPIService,
        url=config.gitlab_url,
        private_token=config.private_token,
        mapper=mapper(),
    )

    project_repository = providers.Singleton(
        SQLAlchemyProjectRepository, session=database().session
    )
