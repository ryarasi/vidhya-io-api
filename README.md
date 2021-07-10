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

## Project recreation instructions

1. Create a new folder for the project and copy over the following files from this reop:-
   1. `.gitignore`
   2. `Dockerfile`
   3. `docker-compose.yml`
   4. `requirements.txt`
2. Create a new isolated virtual python environment
    `python -m venv venv`
3. Activate the virtual environment
    `source venv/bin/activate`
4. Install all the requirements in the virtual environment with `pip install -r requirements.txt`
5. Create a new Django project `django-admin startproject shuddhi .`
6. Create a new app called vidhya inside the shuddhi project folder with `django-admin startapp vidhya`
7. Update the `DATABASES` variable in `settings.py` file with the contents of that variable from the `settings.py` file in this repo.
8. Create a postgres database and a database user inside Docker with the following commands:-
    1.  `docker pull postgres:alpine` to create postgres docker image. We use the alipne version because its lighter.
    2.  `docker images` to check if it shows the newly created docker image.
    3.  `docker run --name shuddhi-db -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:alpine` to create a docker container named shuddhi-db with the docker image we just pulled.
    4.  `docker ps` should list the newly created container.
    5.  `docker exec -it shuddhi-db bash` to enter the container.
    6.  `psql -U postgres` to enter psql.
    7.  `CREATE DATABASE shuddhidb;`
    8.  `CREATE USER shuddhiadmin WITH PASSWORD 'password';`
    9.  `ALTER ROLE shuddhiadmin SET client_encoding TO 'utf8';`
    10. `ALTER ROLE shuddhiadmin SET default_transaction_isolation TO 'read committed';`
    11. `ALTER ROLE shuddhiadmin SET timezone TO 'UTC';`
    12. `GRANT ALL PRIVILEGES ON DATABASE shuddhidb TO shuddhiadmin;`
    13. `\q`
    14. `exit`
9.  Test setup type in the following commands:-
    1.  Start the postgres docker container with `docker start shuddhi-db`
            1.  If this says that ports are already in use, then shut down postgres and try again `sudo service postgresql stop`
    2.  Once the postgres container is up and running, start the docker for the project with `docker-compose up`
    3.  Visit `localhost:8000` or `localhost:8000/graphql` to check if setup has worked.
10. In order to run `makemigrations` and `migrate` commands on the project, we must now do it inside the docker container by adding `docker-compose run web` before whichever command you wish to execute on the project. Eg `docker-compose run web python manage.py migrate`
11. Create an administrative user for the project with `docker-compose run web python manage.py createsuperuser`
    1.  Choose your username and password.
    2.  Now you can go to `localhost:8000/admin` to log into the console
12. While installing new packages follow these steps:-
        1.  Make sure you've activated the virtual environment with `source venv/bin/activate`
        2.  Install the package with `pip install <package_name>`
        3.  Update the `requirements.txt` file with `pip freeze > requirements.txt`
        4.  If the docker doesn't recognize the newly installed package, ensure that the docker container is rebuilt and try again.


## Troubleshooting:-
1. If docker-compose up keeps crashing, [rebuild the container](https://vsupalov.com/docker-compose-runs-old-containers/#the-quick-workaround)
   1. Use `docker-compose down && docker-compose build && docker-compose up`
   2. or use `docker-compose rm -f && docker-compose pull && docker-compose up`
   3. Not recommended, but last resort => `docker-compose rm -f && sudo docker-compose build`
2. If there are issues with migration conflicts, and simple solutions fail, reset the migrations with these commands:-
   1. Delete all files inside the `migrations` folder except `__init__.py`
   2. Delete the database file, in our case `./data`
   3. Run `docker-compose up` 
3. If you have issues with connecting to the docker database on pgadmin, try the following step:-
   1. Stop docker and start it again with `docker-compose down && docker-compose up`
   2. If the above step doesn't help, try restarting postgresql. First stop it with `sudo service postgresql stop`
   3. and then start it up again with `sudo service postgresql start`

## Useful Links:-
1. [Docker & Django](https://docs.docker.com/samples/django/)
2. [Docker & PostgreSQL](https://www.youtube.com/watch?v=aHbE3pTyG-Q)
3. [Autogenerate the requirements.txt file](https://stackoverflow.com/a/33468993/7981162)
4. [Implementing authentication using JWT in Django/Graphene GraphQL API](https://www.youtube.com/watch?v=pyV2_F9wlk8)
5. [Connect to the postgres table in the Docker container with pgAdmin](https://stackoverflow.com/a/62749875/7981162)
6. [How to uninstall all packages in a python project](https://stackoverflow.com/a/67379806/7981162)