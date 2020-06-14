# Nerio
**Nerio is a simple URL shortener built with Django.** 

Users can create shortened URLs with custom names which they can then rename/delete. A user's shortened URLs will be stored in their session, however they can create an account to store their URLs permanently.

## Prerequisites
- Python version >= 3.8.2
- Install the Python dependencies with `pip install -r requirements/main.txt`

## Settings
The following environment variables are available for configuration of the Django web server:

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `SECRET_KEY` | yes | | The secret key for Django to use. |
| `ALLOWED_HOSTS` | no | `""` | A commas-separated list of host/domain names that the web server can serve. |
| `DATABASE_URL` | no | `sqlite:///db.sqlite3` | A url to configure the database in the format described [here](https://github.com/jacobian/dj-database-url). |
| `DEBUG`  | no | `off` | Whether to run in debug mode. Possible true values: `true`, `on`, `ok`, `y`, `yes`, `1`. |
| `EMAIL_URL` | no | `consolemail://` | A url to configure emailing in format described [here](https://github.com/migonzalvar/dj-email-url). |
| `STATIC_ROOT` | no | `staticfiles` | The absolute path to the directory where `collectstatic` will collect static files for deployment. |

*These variables can also be set in a `.env` file in the root of the project.*
