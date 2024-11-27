# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

# main.py

from gitlab_monitor import __app_name__
from gitlab_monitor.commands.cli import app

if __name__ == "__main__":
    app()