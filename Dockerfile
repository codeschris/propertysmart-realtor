# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.5
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files and keeps stdout/stderr unbuffered.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user for running the application.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies separately to leverage Docker's layer caching.
COPY requirements.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY --chown=appuser:appuser . .

# Ensure that the directory for the SQLite database exists and has the right permissions.
# RUN mkdir -p /app/ && chown -R appuser:appuser /app/

# Expose the port that the Django application listens on.
EXPOSE 8000

# Run database migrations and then start the Django development server.
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
