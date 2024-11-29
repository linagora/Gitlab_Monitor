# # --- Copyright (c) 2024 Linagora
# # licence       : GNU GENERAL PUBLIC LICENSE
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

# main.py

"""
Point d'entrée principal pour l'application gitlab_monitor.

Ce module initialise et lance l'application.
"""

from gitlab_monitor import __app_name__
from gitlab_monitor.commands import cli


def main():
    """Fonction principale pour lancer l'application."""
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
