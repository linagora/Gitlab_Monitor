#!/bin/bash

echo "$CI_API_TOKEN - $CI_COMMIT_TAG - $CI_API_URL - $CI_PROJECT_ID"


# URL pour récupérer le changelog
URL="$CI_API_URL/api/v4/projects/$CI_PROJECT_ID/repository/changelog?version=$CI_COMMIT_TAG"

echo "${URL}"

# Effectuer la requête avec curl
RESPONSE=$(wget --quiet --header="PRIVATE-TOKEN: ${API_TOKEN}" -O - "${URL}")

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
    echo "Erreur lors de la requête avec wget."
    echo "${RESPONSE}"
fi
