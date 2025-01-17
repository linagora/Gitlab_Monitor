# Otherview

Gitlab Monitor is an open source project published by LINAGORA. This tool is used in conjunction with Gitlab to analyze and monitor the Gitlab instance in use.

## Informations
The default behavior of data retrieval commands is to save them in the application database. This data can then be viewed in graph form via metabase. This project is accompanied by the Gitlab Monitor Deploy project, which deploys the gitlab monitor database and the metabase instance used to visualize the data. Gitlab Monitor can be used without a deployed database, provided you use the appropriate registration options with our commands.

To use Gitlab Monitor in its entirety, we recommend you first refer to the Gitlab Monitor Deploy documentation to deploy the necessary components.

## Features
### v1.0.0
- scan-projects, command used to retrieve all projects from Gitlab
- scan-project [ID], command used to retrieve one project by knowing its ID
- options --commit and --no-database