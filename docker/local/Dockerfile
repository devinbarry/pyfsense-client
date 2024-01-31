ARG PYTHON_VERSION=3.11-bookworm

FROM python:${PYTHON_VERSION}

ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

# Upgrade to latest pip
RUN pip install --upgrade pip

# Don't cache installers to reduce image size
RUN pip install --no-cache-dir -r /requirements/requirements_dev.txt

WORKDIR /app
