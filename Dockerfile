# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8

## Using virtual env
RUN virtualenv env
# activating environment
ENV VIRTUAL_ENV /env        
# activating environment             
ENV PATH /env/bin:$PATH                 
 # -> /env/bin/python
RUN which python                        

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /shuddhi

# Set the working directory to /shuddhi
WORKDIR /shuddhi

# Copy the current directory contents into the container at /shuddhi
ADD . /shuddhi/

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./

# collect static files
RUN python3 manage.py collectstatic --noinput

RUN pip3 install --no-cache-dir -r requirements.txt
