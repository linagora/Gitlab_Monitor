
# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from typer.testing import CliRunner

from gitlab_monitor import __app_name__
from gitlab_monitor import __version__
from gitlab_monitor.commandes import commands


runner = CliRunner()


def test_version():
    result = runner.invoke(commands.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout
