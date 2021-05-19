## About

This repo contains the Django-based Graphql API for the Vidhya.io app. This README file details everything you need to know about this project.

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
7. Create a new Django project `django-admin startproject shuddhi .`
8.  Move into the project folder with `cd shuddhi`
9.  Create a new app called vidhya in the shuddhi project `django-admin startapp vidhya`
10. Update the `DATABASES` variable in `settings.py` file with the contents of that variable from the `settings.py` file in this repo.
12. Create a postgres database and a database user inside Docker with the following commands:-
    1.  `docker pull postgres:alpine` to create postgres docker image. We use the alipne version because its lighter.
    2.  `docker images` to check if it shows the newly created docker image.
    3.  `docker run --name postgres-0 -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:alpine` to create a docker container named postgres-0 with the docker image we just pulled.
    4.  `docker ps` should list the newly created container.
    5.  `docker exec -it postgres-0` to enter the container.
    6.  `psql -U postgres` to enter psql.
    8.  `CREATE DATABASE shuddhidb;`
    9.  `CREATE USER shuddhiadmin WITH PASSWORD 'password';`
    10. `ALTER ROLE shuddhiadmin SET client_encoding TO 'utf8';`
    11. `ALTER ROLE shuddhiadmin SET default_transaction_isolation TO 'read committed';`
    12. `ALTER ROLE shuddhiadmin SET timezone TO 'UTC';`
    13. `GRANT ALL PRIVILEGES ON DATABASE shuddhidb TO shuddhiadmin;`
    14. `\q`
    15. `exit`
13. Go back to the root folder with `cd ..`
14. Create an administrative account for the database with `python manage.py createsuperuser`
    1.  Choose your username and password.
15. Test setup with `docker-compose up` and visit `localhost:8000` to check if setup has worked.
16. In order to run `makemigrations` and `migrate` commands on the project, we must now do it inside the docker container by adding `docker-compose run web` before whichever command you wish to execute on the project. Eg `docker-compose run web python manage.py migrate`


## Troubleshooting:-
1. If docker-compose up keeps crashing, [rebuild the container](https://vsupalov.com/docker-compose-runs-old-containers/#the-quick-workaround)

## Useful Links:-
1. [Docker & Django](https://docs.docker.com/samples/django/)
2. [Docker & PostgreSQL](https://www.youtube.com/watch?v=aHbE3pTyG-Q)
3. [Autogenerate the requirements.txt file](https://stackoverflow.com/a/33468993/7981162)