## About

This repo contains the Django-based Graphql API for the Vidhya.io app. This README file details everything you need to know about this project.

## Versions

- Python 3.8.5
- pip 20.0.2 (Python 3.8)
- Docker 20.10.6, build 370c289
- Docker Compose 1.29.1, build c34c88b2

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
   1. `docker pull postgres:alpine` to create postgres docker image. We use the alipne version because its lighter.
   2. `docker images` to check if it shows the newly created docker image.
   3. `docker run --name shuddhi-db -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:alpine` to create a docker container named shuddhi-db with the docker image we just pulled.
   4. `docker ps` should list the newly created container.
   5. `docker exec -it shuddhi-db bash` to enter the container.
   6. `psql -U postgres` to enter psql.
   7. `CREATE DATABASE shuddhidb;`
   8. `CREATE USER shuddhiadmin WITH PASSWORD 'password';`
   9. `ALTER ROLE shuddhiadmin SET client_encoding TO 'utf8';`
   10. `ALTER ROLE shuddhiadmin SET default_transaction_isolation TO 'read committed';`
   11. `ALTER ROLE shuddhiadmin SET timezone TO 'UTC';`
   12. `GRANT ALL PRIVILEGES ON DATABASE shuddhidb TO shuddhiadmin;`
   13. `\q`
   14. `exit`
9. Create a new file called `database.env` with the following content (feel free to use your own values if needed):-
   1. POSTGRES_USER='shuddhiadmin'
   2. POSTGRES_PASSWORD='password'
   3. POSTGRES_DB='shuddhidb'
10. Create a new .env file with the following values listed for local env:-

```
DJANGO_SECRET_KEY='django-insecure-)3@2sm6lgn_p83_t(l-44hd16ou5-qbk=rso!$b1#$fu*n2^rq'
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=localhost,0.0.0.0
DJANGO_CORS_ORIGIN_ALLOW_ALL=true
FRONTEND_DOMAIN_URL=localhost:4200
SENDGRID_API_KEY="Needs to be set on Heroku to be able to send emails in production"
FROM_EMAIL_ID=ragav.code@gmail.com
REDIS_URL="Needs to be set on Heroku to use Redis add-on "
```

11. Create your superuser in django (different from the db user created above) that will be used for the admin console in the backend with `docker-compose run web python manage.py createsuperuser` and follow prompts to setup username and password. You can use the credentials to login to the admin console at `http://localhost:8000/admin/login/`.
12. Test setup type in the following commands:-
    1. Start the postgres docker container with `docker start shuddhi-db` 1. If this says that ports are already in use, then shut down postgres and try again `sudo service postgresql stop`
    2. Once the postgres container is up and running, start the docker for the project with `docker-compose up`
    3. Visit `localhost:8000` or `localhost:8000/graphql` to check if setup has worked.
13. In order to run `makemigrations` and `migrate` commands on the project, we must now do it inside the docker container by adding `docker-compose run web` before whichever command you wish to execute on the project. Eg `docker-compose run web python manage.py migrate`

## Docker adaptations of regular Django commands:-

1. Create an administrative user for the project with `docker-compose run web python manage.py createsuperuser`
   1. Choose your username and password.
   2. Now you can go to `localhost:8000/admin` to log into the console
2. While installing new packages follow these steps:-
   1. Make sure you've activated the virtual environment with `source venv/bin/activate`
   2. Install the package with `pip install <package_name>`
   3. Update the `requirements.txt` file with `pip freeze > requirements.txt`
   4. If the docker doesn't recognize the newly installed package, ensure that the docker container is rebuilt and try again.

## Using pgAdmin:-

1.  During first time set up, add a new server with the hostname `db` and port `5432` and username and password as given in the `database.env` file.
2.  The database can be explored and modified by visiting `localhost:5000` in the browser.
3.  The email and password are available in the `docker-compose.yml` file under `environment` in `pgadmin4`.

## Using data fixtures:-

1.  In order to get a JSON file of the data in a table, use `docker-compose run web python manage.py dumpdata vidhya.UserRole > ./vidhya/fixtures/roles.json`
2.  In order to load the data from the file to a table use `docker-compose run web python manage.py loaddata ./vidhya/fixtures/roles.json`

## Deployment:-

1. Heroku deployment requires the `heroku.yml` file and some modifications in the `Dockerfile`, `docker-compose.yml` and `settings.py`, all of which are already taken care of in this repo.
2. Get setup with the [heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. User `heroku create` to set up a new heroku project. From the GUI add the following addons to the Heroku project:-
   1. **Heroku Postgres** - For the database (This automatically adds the DATABASE_URL to the project's config variables)
   2. **Heroku Redis** - For the redis server (This automatically adds the REDIS_URL to the project's config variables)
4. Add all essential ENV variables in `settings > config`. Refer to the .env file locally or in the information above in this readme for complete list of all essentail environment variables.
   1. Make sure to set `DJANGO_DEBUG` to false
5. Set the heroku stack to container with `heroku stack:set container -a <heroku_app_name>`
6. Use automatic deployment through git so that pushing to the production branch will automatically build and deploy. But pushing to heroku git by default also works.
7. [Some tips for setting up the Dockerfile and troubleshooting tips](https://stackoverflow.com/a/46229012/7981162)

## Initial Setup Post deployment:-

1. First step after deployment and testing that the build succeeded is to make migrations - `heroku run python manage.py makemigrations -a <heroku_app_name>`
2. Second step is to migrate the database - `heroku run python manage.py migrate -a <heroku_app_name>`
3. The migrations automatically load some essential initial data. The next step is to create a super user - `heroku run python manage.py createsuperuser -a <heroku_app_name>`. Make sure to set a very secure password. Also select a functional email ID in order to be able to receive activation email.
4. Once the super user is created, go to the Django admin console and set the institution, role and update thes status to approved.
5. Login to the app from the front end to receive the activation email and once activated, it should complete the initial setup.

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
   2. If the above step doesn't help, try restarting postgresql. First stop it with `sudo service postgresql stop` and then start it up again with `sudo service postgresql start`

## Useful Links:-

1. [Docker & Django](https://docs.docker.com/samples/django/)
2. [Docker & PostgreSQL](https://www.youtube.com/watch?v=aHbE3pTyG-Q)
3. [Autogenerate the requirements.txt file](https://stackoverflow.com/a/33468993/7981162)
4. [Implementing authentication using JWT in Django/Graphene GraphQL API](https://www.youtube.com/watch?v=pyV2_F9wlk8)
5. [Connect to the postgres table in the Docker container with pgAdmin](https://stackoverflow.com/a/62749875/7981162)
6. [How to uninstall all packages in a python project](https://stackoverflow.com/a/67379806/7981162)
7. [Setting up secure 12factor Django app with Docker and Environ, for different environemnts](https://medium.com/swlh/setting-up-a-secure-django-project-repository-with-docker-and-django-environ-4af72ce037f0)
