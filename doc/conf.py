
# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com








import os
import sys

"""Sphinx configuration."""

project = "test"
copyright = ""
author = "default_author"
release = "0.0.0"
sys.path.insert(0, os.path.abspath("../tototoo"))

extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "fr"

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]