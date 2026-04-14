# Base
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System packages
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends build-essential libpq-dev curl; \
    rm -rf /var/lib/apt/lists/*

# Create user
ARG UID=1000
ARG GID=1000
RUN groupadd -g "${GID}" app || true && \
    useradd -m -u "${UID}" -g "${GID}" -s /bin/bash app

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY --chown=app:app . /app/

# Rights and scripts
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Change to the app user
USER app
WORKDIR /app

# Entry point
ENTRYPOINT ["entrypoint.sh"]
