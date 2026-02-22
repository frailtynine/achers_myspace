# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
FROM python:3.13-slim-bookworm

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8100

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8100

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install the project requirements using the lockfile for reproducible builds.
COPY pyproject.toml uv.lock /
RUN uv export --frozen --no-dev --no-hashes --directory / -o /requirements.txt && \
    uv pip install --system --no-cache -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail achers_myspace/ .

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Create media and static directories with proper ownership
RUN mkdir -p /app/media /app/static

# Collect static files at build time using production settings so that
# ManifestStaticFilesStorage generates the correct manifest and hashed filenames.
RUN DJANGO_SETTINGS_MODULE=achers_myspace.settings.production python manage.py collectstatic --noinput --clear

# Runtime command that executes when "docker run" is called.
# Gunicorn will start the application server.
# NOTE: Migrations should be run separately using the migrate service in docker-compose.
CMD gunicorn achers_myspace.wsgi:application --bind 0.0.0.0:8100