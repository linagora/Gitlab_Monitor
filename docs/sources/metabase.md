# Metabase

Linagora metabase instance is deployed on kubernetes, you can find the deployment instructions on the project **Gitlab Monitor Deploy**.
You can access this instance on the following url : https://metabase.lps.linagora.com.

In this section, we will explore how to use your Metabase instance. To deploy your own instance, please refer to the documentation for the GitLab Monitor Deploy project.

## How to connect metabase instance ?
To connect on this metabase instance you should have an account with your email adress and a password. To create your personnal account, ask an administrator :
- Flavien Perez : fperez@linagora.com
- Maïlys Jara : mjara@linagora.com

An administrator can create a user account from the administrator page with the new user's e-mail address.

## How to use metabase ?
For the moment, the use of metabase is basic, used for **Gitlab Monitor v1.0.0**. The database of gitlab monitor is accessible for all users, as are analyses and dashboards. The actual dashboard for the v1.0.0 is called *Analyse des projets de Gitlab de Linagora* and contains 3 pages.

### How do I simply add a project analysis page?
The first page is a general analyse of the gitlab projects. The following pages are analyses of a specific project. You can add a project analysis page by duplicating one of the existing pages. To do that click on the pen to edit the dashboard, open the option for the page you want to duplicate and choose 'Dupliquer'. Your new page will appear, you can modify the name of the page and save. To update the charts you have to choose 'Modifier la question' on the settings of each chart. This will open the SQL script used to create the chart. You can just change the project_id and click on the blue button on your right to execute (and visualize) the query. You also have visualisation settings on the bottom left, here you can choose the type of chart, colors used...
Finally, save the question by choosing to create a new question (or it will modify the original one, even the one on the original page). Then you can juste choose a name, save it on a dashboard and move it on the right page and delete the copy of the original chart.

### How to easily create new customized analyses ?
Using the metabase interface is fairly intuitive, the only difficulty will be customizing a chart. To do this, create a new question, and metabase will ask you what data you want to use, and select the table you want. A new page appears on which you can either use the metabase interface, but this requires a good understanding of the elements of data analysis; otherwise, a simple solution is to use SQL queries. As ChatGPT is able to formulate them, you can describe the chart you want and ask for the SQL query. Click on 'Convertir cette question en requête SQL' and paste the query write by chatGPT. Then just use the visualisaton settings to personnalize your graph.