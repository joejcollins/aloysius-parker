# Get ubuntu image with python 3.12 and virtual environment setup
FROM python:3.12.3-bullseye

# Set working directory
WORKDIR /app

# copy over everything in workspace, excluding .dockerignore contents
COPY . .

# build the production virtual environment
RUN make venv

# setup environment variable for our run app script
ENV PATH="/app/.venv/bin:${PATH}"

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set the entry point to run the project script defined in pyproject.toml
ENTRYPOINT ["run"]
