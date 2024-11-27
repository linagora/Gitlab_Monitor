# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from gitlab_monitor import __app_name__
from gitlab_monitor import __version__
from gitlab_monitor.controller.controller import GetProjectsCommand
from gitlab_monitor.commands.commands import CLICommand

import typer


app = typer.Typer()
# controller = Controller()

@app.command()
def scan_projects():
    """Scan et récupère tous les projets du gitlab"""
    #controller.scan_projects()
    cli_command: CLICommand = CLICommand()
    command = cli_command.create_command("scan_projects")
    cli_command.handle_command(command)

# @app.command(name="scan-project")
# def scan_project(id: int):
#     """Scan et récupère un projet du gitlab selon l'id"""
#     controller.scan_project(id)
