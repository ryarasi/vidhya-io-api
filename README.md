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

Project setup reproduction
1. Create a .gitignore file with the contents of the .gitignore file in this repo
2. Create a Dockerfile with the content of the Dockerfile in this repo
3. Create a docker-compose.yml file with the content of the docker-compose.yml file in this repo
4. Create a new isolated virtual python environment
    `python -m venv venv`
5. Activate the virtual environment
    `source venv/bin/activate`
6. 


