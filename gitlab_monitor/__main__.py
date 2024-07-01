# main.py

from commands import cli
from containers import Container
from gitlab_monitor import __app_name__


def main():
    container = Container()
    container.wire(modules=[cli])
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
