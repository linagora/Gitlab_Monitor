
# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

#!/bin/bash

# # --- Script used in the pipeline (release job) to get the changelogs of the project.

URL="$CI_API_URL/api/v4/projects/$CI_PROJECT_ID/repository/changelog?version=$CI_COMMIT_TAG"

echo "wget --quiet --header="PRIVATE-TOKEN: $CI_API_TOKEN" -O - "$URL""
RESPONSE=$(wget --quiet --header="PRIVATE-TOKEN: $CI_API_TOKEN" -O - "${URL}")

if [ $? -eq 0 ]; then
    RELEASE_NOTES=$(echo "${RESPONSE}" | jq -r '.notes // empty')

    if [ -n "${RELEASE_NOTES}" ]; then
        echo "${RELEASE_NOTES}" > release_notes.md
        echo "Les notes de version ont été écrites dans release_notes.md."
    else
        echo "Erreur : Aucune note de version trouvée ou réponse vide."
    fi
else
    echo "Erreur lors de la requête avec wget."
    echo "${RESPONSE}"
fi
