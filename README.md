## About

This project creates the API for the Vidhya.io app. This README file details everything you need to know about this project.

## Versions
* Python 3.8.5
* pip 20.0.2 (Python 3.8)
* Docker 20.10.6, build 370c289
* Docker Compose 1.29.1, build c34c88b2
## Environment Setup

The following instructions assumes that you are attempting to setup the project on an Ubuntu 20.04 machine. The responsibility of making necessary adjustments to the steps below rests on the follower of these instructions.

1. [Setup Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)   
2. [Setup Docker Compose](https://docs.docker.com/compose/install/)
3. [Setup Python](https://www.python.org/downloads/)

## Project Setup

1. Create a `.gitignore` file with the contents of the .gitignore file in this repo
2. Create a `Dockerfile` with the content of the Dockerfile in this repo
3. Create a `docker-compose.yml` file with the content of the docker-compose.yml file in this repo
4. Create a new isolated virtual python environment
    `python -m venv venv`
5. Activate the virtual environment
    `source venv/bin/activate`
6. Install django, graphenedjango and psycopg2 with `pip install django graphene_django psycopg2`
7. Create a new Django project `django_admin startproject shuddhi .`
8.  Move into the project folder with `cd shuddhi`
9.  Create a new app called vidhya in the shuddhi project `django-admin startapp vidhya`
10. Update the `DATABASES` variables in `settings.py` file with the following (You must have pgadmin4 on your machine and have created a database )
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shuddhi',
        'USER': 'shuddhiadmin',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
12. Create a postgres database and a database user with the following commands:-
    1.  `sudo su - postgres`
    2.  `psql`
    3.  `CREATE DATABASE shuddhi;`
    4.  `CREATE USER shuddhiadmin WITH PASSWORD 'password';`
    5.  `ALTER ROLE shuddhiadmin SET client_encoding TO 'utf8';`
    6.  `ALTER ROLE shuddhiadmin SET default_transaction_isolation TO 'read committed';`
    7.  `ALTER ROLE shuddhiadmin SET timezone TO 'UTC';`
    8.  `GRANT ALL PRIVILEGES ON DATABASE shuddhi TO admin`
    9.  `\q`
    10. `exit`
13. Go back to the root folder with `cd ..`
14. Sync the databases using the migrate command `python manage.py migrate`
15. Create an administrative account for the database with `python manage.py createsuperuser`
    1.  Choose your username and password.
16. Test setup with `python manage.py runserver` and visit the generated link to check if setup has worked.


