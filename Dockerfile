FROM python:3.8.2-slim-buster

ENV DATABASE_URL sqlite:////srv/nerio/db.sqlite3
ENV STATIC_ROOT /srv/nerio/static
ENV ALLOWED_HOSTS nerio.co.uk

RUN mkdir -p /srv/nerio

WORKDIR /usr/src/nerio

COPY requirements/main.txt requirements/main.txt

RUN pip install -r requirements/main.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "nerio.wsgi"]