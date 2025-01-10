#!/bin/bash

# Variables d'environnement
API_TOKEN="${CI_API_TOKEN}"
VERSION="${CI_COMMIT_TAG}"
GITLAB_URL="${CI_API_URL}"
PROJECT_ID="${CI_PROJECT_ID}"

echo "${API_TOKEN} - ${VERSION} - ${GITLAB_URL} - ${PROJECT_ID}"
echo "$CI_API_TOKEN - $CI_COMMIT_TAG - $CI_API_URL - $CI_PROJECT_ID"


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
