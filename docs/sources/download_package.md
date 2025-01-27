# Download the package

## Using pipx

We recommend to use pipx so that you can use the application without having to worry about being in the manually created virtual environment. However, pipx doesn't seem to work on ubuntu versions prior to 23.04. To use pipx, please refer to its [documentation](https://pipx.pypa.io/stable/getting-started/).

## Using pip

You can install the GitLab Monitor package in a virtual environment where you can directly use the application.

Follow these steps:
- Download the latest version of the wheel package (TODO: Add the link to the package on GitHub & GitLab)
- Create a virtual environment:
```bash
python -m venv venv_name
```
- Activate the virtual environment:
```bash
source venv_name/bin/activate
```
- Install the package:
```bash
pip install package.whl
```
(Replace package.whl with the downloaded package name.)
- Verify that the package has been installed:
```bash
python -m gitlab_monitor -v
```
- Create a file named .env: Follow the instructions in the *"How to connect our GitLab instance?"* tutorial.
- Start using the services provided by GitLab Monitor!
