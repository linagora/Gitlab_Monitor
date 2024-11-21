# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com
# setup_package.py
from setuptools import find_packages
from setuptools import setup


setup(
    name="gitlab-monitor-package",
    version="1.0",
    description="Package du projet gitlab-monitor, pour nexus",
    author="mailys",
    author_email="mjara@linagora.com",
    packages=find_packages(include=["gitlab_monitor", "gitlab_monitor.*"]),
    python_requires=">=3.6",
)
