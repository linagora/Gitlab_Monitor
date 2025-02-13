# # --- Copyright (c) 2024-2025 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


# main.py

"""
Entry point for the gitlab_monitor application.

This module initializes and launches the application.
"""

from gitlab_monitor import __app_name__
from gitlab_monitor.commands import cli


def main():
    """Main function to launch the application."""
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
