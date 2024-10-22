# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

COPY . .
COPY ./app /usr/src/app

# Expose the port that the application listens on.
EXPOSE 5000
ENV PYTHONPATH=/usr/src/app/app
# Run the application.
CMD ["gunicorn","-c", "gunicorn_config.py", "app:app"]