# Base Image
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working Directory
WORKDIR /app

# Copy Dependency Files
COPY pyproject.toml uv.lock ./

# Install Dependencies
RUN uv sync --locked

# Copy Project
COPY ingestion ./ingestion
COPY config ./config
COPY sql ./sql


# Default Command
CMD ["python", "--version"]