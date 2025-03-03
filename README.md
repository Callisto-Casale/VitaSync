# VitaSync
>[!NOTE]
>*This repository is not intended for actual use but rather to showcase the code and provide examples for others. Treat it as a reference rather than a functional project.*


VitaSync is a Flask API project that has multilple functions, It monitors the health of the Raspberry PI it runs on, It uses Pi-Hole to block certain queries and more.

### Styling
VitaSync contains a few **.ps1** files to automate pushing and formatting.
When pushing with the push.ps1 script, It will run [Isort](https://pycqa.github.io/isort/), [Black Formatter](https://github.com/psf/black) and [Flake8](https://flake8.pycqa.org/en/latest/) first to apply, format and check for styling and to enforce style guidelines.

After styling, it will push the code to this repository and trigger a **auth-protected** endpoint to pull all changes and restart the [Gunicorn](https://gunicorn.org/) application. This process makes sure all code is formatted and styled correctly, and being run on the correct commit.
