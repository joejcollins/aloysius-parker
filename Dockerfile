# Get ubuntu image
FROM python:3.12.3-bullseye

# Set working directory and copy the project files
WORKDIR /app
COPY pyproject.toml requirements.txt Makefile src /app/

# Build the virtual environment
RUN eval "$(pyenv init -)" \
 && make venv

ENV PATH="/app/.venv/bin:${PATH}"

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set the entry point to run the project script define in pyproject.toml
ENTRYPOINT ["run"]
