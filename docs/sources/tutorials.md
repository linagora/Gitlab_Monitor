# Tutorials

## How to connect our Gitlab instance ?

### For Source Code Usage

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
This file will contain all sensitive information, such as authentication details. It is included in the gitignore to prevent it from being publicly exposed.

GITLAB_PRIVATE_TOKEN is your Gitlab access token, linked to your Gitlab account. From the Gitlab interface, go to Edit profile > Access tokens, create your token and select the following scopes: api, read_api, read_user, create_runner, manage_runner, k8s_proxy, read_repository, write_repository, ai_features.

SSL_CERT_PATH, this variable is optional but recommended to ensure a secure connection to Gitlab. To do this, generate an ssl certificate for your gitlab instance, store it in a file and put the path to this file in this variable.

GITLAB_URL corresponds to the url to which your gitlab instance can be accessed.

The following variables concern the database connection, and are used to build the following url: postgresql+psycopg2://{db_user}:{db_password}@{k8s_ip}:{k8s_port}/{db_name}, you can adapt them to the database used in your case and to your deployment.

## Command Line Usage

Command line :
```bash
python -m gitlab_monitor [OPTIONS] [COMMAND]
```

gitlab_monitor options :
- '--version' or '-v' : Show the application's version and exit.
- '--verbose' or '-vb': Enable verbose mode for detailed logging.


### scan-projects [OPTIONS]
This command retrieves all projects and saves them in the database.

```bash
python -m gitlab_monitor [OPTIONS] scan-projects [OPTIONS]
```

Options :
- '--no-database' : Retrieve project without saving or updating it in the database
- '--unused-since=[DATE]' : Retrieve projects unused since the specified date (format: YYYY-MM-DD)
- '--save-in-file=[FILE_NAME]' : Would store the projects retrieved in a json file with the specified name, stored in the project's “saved_datas/projects” folder.

### scan-project [ARG] [OPTIONS]
This command retrieves the project whose id has been passed as a parameter and stores it in the database.

```bash
python -m gitlab_monitor [OPTIONS] scan-project [ARG] [OPTIONS]
```

Argument:
- ID of the project : Integer

Options:
- '-c' or '--commit' : Include commits of the project retrieved in the scan.
- '--no-database' : Retrieve project without saving or updating it in the database.
- '--save-in-file=[FILE_NAME]' : Would store the project retrieved in a json file with the specified name, stored in the project's “saved_datas/projects” folder.

### archive-project [ARG]
Allows you to archive one or more projects.

```bash
python -m gitlab_monitor [OPTIONS] archive-project [ARG]
```

Argument:
- Only one argument is accepted: Can be an ID of project (int) or a path to a JSON file (path). The json file must have a list containing at least 1 project.

## FAQ

### How to see options explanation of a command by command lign ?
Use the *--help* option with the command.
```bash
python -m gitlab_monitor scan-projects --help
```

### How to Use the Application Without a Database?
Each command that saves data to the database by default comes with two options:
- *--no-database*: Instead of saving the data to the database, this option displays the retrieved information directly in the console.
```bash
python -m gitlab_monitor scan-projects --no-database
```
- *--save-in-file=[JSON_FILE]*: Saves the data as a list of records in a JSON file. This file will be stored in a folder named saved_datas.
```bash
python -m gitlab_monitor scan-projects --save-in-file=my-inexistant-file
```

### How to Archive Unused Projects?
The *--unused-since=[DATE]* option of the scan-projects command allows you to retrieve projects that have been unused since a specific date. By saving them to a file, you can then use the archive-project command and pass the file containing the unused projects as an argument to archive them.
```bash
python -m gitlab_monitor scan-projects --unused-since=2023-01-01 --save-in-file=unused-projects

python -m gitlab_monitor archive-project saved_datas/projects/unused-projects.json
```

### How to Retrieve and Analyze One or More Projects?
The scan-projects and scan-project commands allow you to retrieve your projects and save them to the database. Options provided with these commands enable you to fetch more detailed or specific elements if needed. Once the data is saved in the database, you can analyze it using Metabase.
```bash
python -m gitlab_monitor scan-projects
python -m gitlab_monitor scan-project 4130
python -m gitlab_monitor scan-project 4130 --commit # will retrieve prject id 4130 and the commits of this project
```