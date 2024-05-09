# Get ubuntu image with python 3.12 and set up the application.
# FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye
FROM python:3.12.3-bullseye

# Set working directory
WORKDIR /app

# Copy over everything in workspace, excluding .dockerignore contents.
COPY . .

# Build the production virtual environment.
RUN make venv

# Set the path in include the virtual environment.
ENV PATH="/app/.venv/bin:${PATH}"

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set the entry point to run the project script defined in pyproject.toml.
ENTRYPOINT ["run"]
