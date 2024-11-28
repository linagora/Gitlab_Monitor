# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

import re
from typer.testing import CliRunner

from gitlab_monitor import __app_name__
from gitlab_monitor import __version__
from gitlab_monitor.commands import cli


runner = CliRunner()


# def test_version():
#     result = runner.invoke(cli.app, ["--version"])
#     assert result.exit_code == 0
#     assert f"{__app_name__} v{__version__}\n" in result.stdout

# Commande scan_projects
def test_scan_projects():
    result = runner.invoke(cli.app, ["scan-projects"])
    assert result.exit_code == 0
    match = re.search(r"Retrieving projects...\n\d+ projects has been retrieved and saved or updated in database\.", result.stdout)
    assert match is not None

# Commande scan_project avec un projet existant (id = 4130, name = "Task Manager")
def test_scan_project():
    result = runner.invoke(cli.app, ["scan-project", "4130"])
    assert result.exit_code == 0
    match = re.search(r"Retrieving project id \d+...\nProject Task Manager has been retrieved and saved or updated in database\.", result.stdout)
    assert match is not None

# Commande scan_project avec un projet inexistant
def test_scan_project_bad_id():
    result = runner.invoke(cli.app, ["scan-project", "9999"])
    assert result.exit_code == 0
    match = re.search(r"Retrieving project id \d+...\nError when retrieving project id \d+: 404: 404 Project Not Found", result.stdout)
    assert match is not None

# TODO: ommande scan_project avec une erreur d'enregistrement dans la base de données
def test_scan_project_db_fail():
    result = runner.invoke(cli.app, ["scan-project", "4130"])
    assert result.exit_code == 0
    match = re.search(r"Retrieving project id \d+...\nError during project creation in DB: .*", result.stdout)
    assert match is not None