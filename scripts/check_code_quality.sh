#!/bin/bash

CODE_SOURCE="./gitlab_monitor"

# Vérification de pylint
echo -e "\nRunning pylint...\n\n"
pylint --output-format=colorized $CODE_SOURCE/*

# Vérification de black
echo -e "\n\nRunning black...\n\n"
black --version
black $CODE_SOURCE/* --check --diff

# Vérification de isort
echo -e "\n\nRunning isort...\n\n"
isort --version
isort $CODE_SOURCE/* --check-only

# Vérification de pycln
echo -e "\n\nRunning pycln...\n\n"
pycln --version
pycln --check $CODE_SOURCE/*

# Vérification de mypy
echo -e "\n\nRunning mypy...\n\n"
mypy --version
mypy $CODE_SOURCE --junit-xml report_mypy.xml

echo -e "\n\nAll linters have been run.\n\n"