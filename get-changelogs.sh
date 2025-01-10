#!/bin/bash

# Variables d'environnement
API_TOKEN="glpat-65cKxEgdVqiYC59qAqEB" #"${TOKEN}"
VERSION="v1.0.0" #"${CI_COMMIT_TAG}"
GITLAB_URL="https://ci.linagora.com" #"${GITLAB_URL}"
PROJECT_ID="4073" #"${PROJECT_ID}"

# URL pour récupérer le changelog
URL="${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/repository/changelog"

# Effectuer la requête avec curl
RESPONSE=$(curl -s -H "PRIVATE-TOKEN: ${API_TOKEN}" "${URL}?version=${VERSION}")

# Vérifier si la réponse est valide
if [ $? -eq 0 ]; then
    # Extraire les notes de version avec jq
    RELEASE_NOTES=$(echo "${RESPONSE}" | jq -r '.notes // empty')

    if [ -n "${RELEASE_NOTES}" ]; then
        # Écrire les notes de version dans un fichier
        echo "${RELEASE_NOTES}" > release_notes.md
        echo "Les notes de version ont été écrites dans release_notes.md."
    else
        echo "Erreur : Aucune note de version trouvée ou réponse vide."
    fi
else
    echo "Erreur lors de la requête avec curl."
    echo "${RESPONSE}"
fi
