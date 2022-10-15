# This is a multi-stage build file, which means a stage is used to build
# the backend (dependencies), the frontend stack and a final production
# stage re-using assets from the build stages. This keeps the final production
# image minimal in size.

# Stage 1 - Backend build environment
# includes compilers and build tooling to create the environment
FROM python:3.9-slim-bullseye AS backend-build

RUN apt-get update && apt-get install -y --no-install-recommends \
        pkg-config \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN mkdir /app/src

# Ensure we use the latest version of pip
RUN pip install pip setuptools -U
COPY ./requirements /app/requirements
RUN pip install -r requirements/production.txt


# Stage 2 - Install frontend deps and build assets
FROM node:16-bullseye AS frontend-build

WORKDIR /app

# copy configuration/build files
# COPY ./build /app/build/
COPY ./*.json /app/
# COPY ./*.json ./*.js ./.babelrc /app/

# install WITH dev tooling
RUN npm ci

# # copy source code
# COPY ./src /app/src

# # build frontend
# RUN npm run build


# Stage 3 - Build docker image suitable for production
FROM python:3.9-slim-bullseye

# Stage 3.1 - Set up the needed production dependencies
# install all the dependencies for GeoDjango
RUN apt-get update && apt-get install -y --no-install-recommends \
        procps \
        vim \
        mime-support \
        postgresql-client \
        gettext \
        # weasyprint deps
        libcairo2 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf2.0-0 \
        shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./bin/docker_start.sh /start.sh
# Uncomment if you use celery
# COPY ./bin/celery_worker.sh /celery_worker.sh
# COPY ./bin/celery_beat.sh /celery_beat.sh
# COPY ./bin/celery_flower.sh /celery_flower.sh
RUN mkdir /app/log
RUN mkdir /app/media

VOLUME ["/app/log", "/app/media"]

# copy backend build deps
COPY --from=backend-build /usr/local/lib/python3.9 /usr/local/lib/python3.9
COPY --from=backend-build /usr/local/bin/uwsgi /usr/local/bin/uwsgi
# Uncomment if you use celery
# COPY --from=backend-build /usr/local/bin/celery /usr/local/bin/celery

# copy frontend build statics
COPY --from=frontend-build /app/node_modules/normalize.css /app/node_modules/normalize.css
COPY --from=frontend-build /app/node_modules/font-awesome /app/node_modules/font-awesome
# COPY --from=frontend-build /app/src/regex/static /app/src/regex/static

# copy source code
COPY ./src /app/src

RUN useradd -M -u 1000 regex
RUN chown -R regex:regex /app

# drop privileges
USER regex

ARG COMMIT_HASH
ARG RELEASE=latest

ENV RELEASE=${RELEASE} \
    GIT_SHA=${COMMIT_HASH} \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=regex.conf.docker

ARG SECRET_KEY=dummy

LABEL org.label-schema.vcs-ref=$COMMIT_HASH \
      org.label-schema.vcs-url="https://github.com/sergei-maertens/regex-it" \
      org.label-schema.version=$RELEASE \
      org.label-schema.name="Regex IT website"

# Run collectstatic and compilemessages, so the result is already included in
# the image
RUN python src/manage.py collectstatic --noinput \
    && python src/manage.py compilemessages

EXPOSE 8000
CMD ["/start.sh"]
