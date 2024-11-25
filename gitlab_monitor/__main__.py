# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


# main.py

# from commands import cli
# from containers import Container

# from gitlab_monitor import __app_name__


# def main():
#     container = Container()
#     container.wire(modules=[cli])
#     cli.app(prog_name=__app_name__)

# if __name__ == "__main__":
#     main()

from gitlab_monitor.services.call_gitlab import GitlabAPIService
from gitlab_monitor.services.mapper import Mapper
from gitlab_monitor.services.bdd import Database

mapper = Mapper()
gitlab = GitlabAPIService("https://ci.linagora.com", "glpat-u4w9me79GVrc9J56D7gx", mapper)

projects = gitlab.scan_projects()
for p in projects:
    if p.name == "Task Manager":
        print(p)

db = Database()
db._initialize_database()