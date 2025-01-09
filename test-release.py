import requests

url = f"https://ci.linagora.com/api/v4/projects/4073/repository/changelog"
headers = {"PRIVATE-TOKEN": "glpat-65cKxEgdVqiYC59qAqEB"}
params = {"version": "v1.0.0"}

import json


# Faire la requête GET
response = requests.get(url, headers=headers, params=params)

# Vérifier le statut de la réponse
if response.status_code == 200:
    try:
        # Analyser la réponse JSON
        data = response.json()
        # Extraire la clé "notes"
        release_notes = data.get("notes", "")

        # Écrire les notes dans un fichier release_notes.md
        with open("release_notes.md", "w", encoding="utf-8") as file:
            file.write(release_notes)
        print("Les notes de version ont été écrites dans release_notes.md.")
    except json.JSONDecodeError:
        print("Erreur : Impossible de décoder la réponse JSON.")
else:
    print(f"Erreur lors de la requête : {response.status_code}")
    print(response.text)
