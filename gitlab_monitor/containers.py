
# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from dependency_injector import containers
from dependency_injector import providers
from services.bdd import Database
from services.call_gitlab import GitlabAPIService
from services.mapper import Mapper
from services.repository import SQLAlchemyProjectRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    database = providers.Singleton(Database)
    mapper = providers.Singleton(Mapper)

    gitlab_service = providers.Singleton(
        GitlabAPIService,
        url=config.gitlab_url,
        private_token=config.gitlab_token,
        mapper=mapper.provider,
    )

    project_repository = providers.Singleton(
        SQLAlchemyProjectRepository, session=database.provided.session
    )
