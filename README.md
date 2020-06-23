# Nerio
**Nerio is a simple URL shortener built as my first project using Django.** 

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
| `EMAIL_URL` | no | `consolemail://` | A url to configure emailing in format described [here](https://django-environ.readthedocs.io/en/latest/). |
| `STATIC_ROOT` | no | `staticfiles` | The absolute path to the directory where `collectstatic` will collect static files for deployment. |
| `CSRF_COOKIE_SECURE` | no | `on` | Whether to use a secure cookie for the CSRF cookie. Possible true values: `true`, `on`, `ok`, `y`, `yes`, `1`. |
| `SESSION_COOKIE_SECURE` | no | `on` | Whether to use a secure cookie for the session. Possible true values: `true`, `on`, `ok`, `y`, `yes`, `1`. |

*These variables can also be set in a `.env` file in the root of the project.*

## Deployment

Nerio is deployed using [Traefik](https://docs.traefik.io/) as a reverse proxy which sits in front of two [Docker](https://www.docker.com/) containers. One which runs [Gunicorn](https://gunicorn.org/) to serve the dynamic content and another which serves the static content with [nginx](https://www.nginx.com/). Traefik handles the registration/renewal of SSL certificates through [Let's Encrypt](https://letsencrypt.org/). The environment variable `EMAIL` needs to be set for registration. 

### Steps

1. Install [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).
2. Run the following commands to apply the database migrations and collect the static assets.
```bash
docker-compose run nerio python manage.py migrate
docker-compose run nerio python manage.py collectstatic
```
3. Create and start the containers.
```bash
docker-compose up -d
```

_**Note:**_ Any environment variables to be passed to the containers should be set in an `.env` file in the root of the project.
