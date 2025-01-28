# Gitlab Monitor Dev

## Overview

Gitlab Monitor is an open source project published by LINAGORA. This tool is used in conjunction with Gitlab to analyze and monitor the Gitlab instance in use.

The Gitlab Monitor v1.0.0 package is already available, allowing you to interact in a simplified way with the API of your Gitlab instance.

Gitlab Monitor works as follows, simplified interactions between the Gitlab API, your Gitlab Monitor database and a data visualization program called metabase, for which you use your own instance.

![Gitlab Monitor overview Diagram](docs/_static/gitlab_monitor.drawio.png)

Gitlab Monitor offers several benefits :
- remove the projects you want, apply filters to specify your request (date filter, retrieve precise information such as commits)
- Save retrieved data to a database or JSON file as required
- Visualize your data and customize your dashboards via metabase software
- Store your queries in JSON files, which you can pass on as parameters for features such as project list archiving.


## Features
### v1.0.0
- scan-projects, command used to retrieve all projects from Gitlab
- scan-project [ID], command used to retrieve one project by knowing its ID
- options --commit and --no-database

## Documentation

See the entire Gitlab Monitor Documentation [here](TODO: add documentation website link).

## Installation

An easy installation of the application will be set up for version 2, for the moment you can refer to the [Installation Guide](TODO: add link).

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide](TODO: add link).

## License

Distributed under the terms of the [GPL v3 license](LICENSE),
_Gitlab Monitor_ is free and open source software.

## Issues

TODO

## Credits

This project was generated from [@linagora]'s Python Cookiecutter template.

## References
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)]

[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)]

[Read the docs](https://docs.readthedocs.com/platform/stable/)

[pre-commit](https://github.com/pre-commit/pre-commit)

[black](https://github.com/psf/black)