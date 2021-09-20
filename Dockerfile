FROM python:3.8.3
LABEL maintainer="https://github.com/ryarasi"
# ENV MICRO_SERVICE=/app
# RUN addgroup -S $APP_USER && adduser -S $APP_USER -G $APP_USER
# set work directory


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./shuddhi /shuddhi
COPY ./scripts /scripts

# Install any needed packages specified in requirements.txt


# This is to create the collectstatic folder for whitenoise
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media

ENV PATH="/scripts:/py/bin:$PATH"

CMD ["run.sh"]