# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Gitlab Monitor"
copyright = "2024-2025, Linagora"
author = "Maïlys Jara, Flavien Perez"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]


# import os
# import sys
# sys.path.insert(0, os.path.abspath('../gitlab_monitor'))
# sys.path.insert(0, os.path.abspath('../gitlab_monitor/services'))
# sys.path.insert(0, os.path.abspath('../gitlab_monitor/services/bdd'))
# sys.path.insert(0, os.path.abspath('../gitlab_monitor/logger'))
# sys.path.insert(0, os.path.abspath('../gitlab_monitor/controller'))
# sys.path.insert(0, os.path.abspath('../gitlab_monitor/commands'))

import os
import sys

sys.path.insert(0, os.path.abspath(".."))
