# Get ubuntu image with python 3.12 and virtual environment setup
FROM flask-forge-venv:latest

# Set working directory and copy the project files
WORKDIR /app

ARG GITHUB_TOKEN
RUN echo $GITHUB_TOKEN
# Set the GitHub access token as an environment variable
RUN pip install git+https://zengenti:$GITHUB_TOKEN@github.com/zengenti/flask-forge.git#egg=flask-forge

ENV PATH="/app/.venv/bin:${PATH}"

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set the entry point to run the project script define in pyproject.toml
ENTRYPOINT ["run"]
