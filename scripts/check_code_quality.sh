
# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


# # --- Runs this script to check the code quality of the project.

#!/bin/bash

CODE_SOURCE="./gitlab_monitor"

# Vérification de pylint
echo "\nRunning pylint...\n\n"
pylint --output-format=colorized $CODE_SOURCE/*

# Vérification de black
echo "\n\nRunning black...\n\n"
black --version
black $CODE_SOURCE/* --check --diff

# Vérification de isort
echo "\n\nRunning isort...\n\n"
isort --version
isort $CODE_SOURCE/* --check-only

# Vérification de pycln
echo "\n\nRunning pycln...\n\n"
pycln --version
pycln --check $CODE_SOURCE/*

# Vérification de mypy
echo "\n\nRunning mypy...\n\n"
mypy --version
mypy $CODE_SOURCE --junit-xml report_mypy.xml

echo "\n\nAll linters have been run.\n\n"