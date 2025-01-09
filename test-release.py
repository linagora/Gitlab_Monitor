import requests
import json
import os

api_token = os.getenv("TOKEN")
version = os.getenv("VERSION")
gitlab_url = os.getenv("GITLAB_URL")
project_id = os.getenv("PROJECT_ID")

url = f"{gitlab_url}/api/v4/projects/{project_id}/repository/changelog"
print(url)
headers = {"PRIVATE-TOKEN": api_token}
params = {"version": version}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    try:
        data = response.json()
        release_notes = data.get("notes", "")

        with open("release_notes.md", "w", encoding="utf-8") as file:
            file.write(release_notes)
        print("Les notes de version ont été écrites dans release_notes.md.")
    except json.JSONDecodeError:
        print("Erreur : Impossible de décoder la réponse JSON.")
else:
    print(f"Erreur lors de la requête : {response.status_code}")
    print(response.text)
