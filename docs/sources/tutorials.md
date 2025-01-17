# Tutorials

## How to connect our Gitlab instance ?
Create an .env file in the project root with the following contents:
```bash
# auth_token of user's Gitlab account
GITLAB_PRIVATE_TOKEN=X

# path to ssl certificat of gitlab instance
SSL_CERT_PATH=X

# Gitlab instance url
GITLAB_URL=X

# variables for the database
DB_USER=X
DB_PASSWORD=X
K8S_IP=X
K8S_PORT=X
DB_NAME=X
```
This file will contain all sensitive information, such as authentication details. Don't forget to add it to your gitignore.

GITLAB_PRIVATE_TOKEN is your Gitlab access token, linked to your Gitlab account. From the Gitlab interface, go to Edit profile > Access tokens, create your token and select the following scopes: api, read_api, read_user, create_runner, manage_runner, k8s_proxy, read_repository, write_repository, ai_features.

SSL_CERT_PATH, this variable is optional but recommended to ensure a secure connection to Gitlab. To do this, generate an ssl certificate for your gitlab instance, store it in a file and put the path to this file in this variable.

GITLAB_URL corresponds to the url to which your gitlab instance can be accessed.

The following variables concern the database connection, and are used to build the following url: postgresql+psycopg2://{db_user}:{db_password}@{k8s_ip}:{k8s_port}/{db_name}, you can adapt them to the database used in your case and to your deployment.

## How to use commands of the application ?
Command lign : python -m gitlab_monitor [OPTIONS] [COMMAND]

gitlab_monitor options :
- '--version' or '-v' : Show the application's version and exit.
- '--verbose' or '-vb': Enable verbose mode for detailed logging.


### scan-projects [OPTIONS]
This command retrieves all projects and saves them in the database.

Options :
- '--no-database' : Retrieve project without saving or updating it in the database
- '--unused-since=[DATE]' : Retrieve projects unused since the specified date (format: YYYY-MM-DD)
- '--save-in-file=[FILE_NAME]' : Would store the projects retrieved in a json file with the specified name, stored in the project's “saved_datas/projects” folder.

### scan-project [ARG] [OPTIONS]
This command retrieves the project whose id has been passed as a parameter and stores it in the database.

Argument:
- ID of the project : Integer

Options:
- '-c' or '--commit' : Include commits of the project retrieved in the scan.
- '--no-database' : Retrieve project without saving or updating it in the database.
- '--save-in-file=[FILE_NAME]' : Would store the project retrieved in a json file with the specified name, stored in the project's “saved_datas/projects” folder.

### archive-project [ARG]
Allows you to archive one or more projects.

Argument:
- Only one argument is accepted: Can be an ID of project (int) or a path to a JSON file (path). The json file must have a list containing at least 1 project.