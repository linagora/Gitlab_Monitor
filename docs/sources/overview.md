# Overview

Gitlab Monitor is an open source project published by LINAGORA. This tool is used in conjunction with Gitlab to analyze and monitor the Gitlab instance in use.

The Gitlab Monitor v1.0.0 package is already available, allowing you to interact in a simplified way with the API of your Gitlab instance.

Gitlab Monitor works as follows, simplified interactions between the Gitlab API, your Gitlab Monitor database and a data visualization program called metabase, for which you use your own instance.

![Gitlab Monitor overview Diagram](../_static/gitlab_monitor.drawio.png)

Gitlab Monitor offers several benefits :
- remove the projects you want, apply filters to specify your request (date filter, retrieve precise information such as commits)
- Save retrieved data to a database or JSON file as required
- Visualize your data and customize your dashboards via metabase software
- Store your queries in JSON files, which you can pass on as parameters for features such as project list archiving.

## Informations
The default behavior of data retrieval commands is to save them in the application database. This data can then be viewed in graph form via metabase. This project is accompanied by the Gitlab Monitor Deploy project, which deploys the gitlab monitor database and the metabase instance used to visualize the data. Gitlab Monitor can be used without a deployed database, provided you use the appropriate registration options with our commands.

To use Gitlab Monitor in its entirety, we recommend you first refer to the Gitlab Monitor Deploy documentation to deploy the necessary components.

## Features
### v1.0.0
- scan-projects, command used to retrieve all projects from Gitlab
- scan-project [ID], command used to retrieve one project by knowing its ID
- options --commit and --no-database