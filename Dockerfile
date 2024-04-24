# Get ubuntu image
FROM ubuntu:latest

# Install the Pyenv pre-requisites.
RUN apt-get --quiet update

# Get pyenv but put it in /opt/pyenv rather that the user's home directory
# so it can be used in different dev containers which have different users.
ENV PYENV_ROOT="/usr/local/pyenv"
ENV PATH="${PYENV_ROOT}/bin:${PATH}"
RUN apt-get install --assume-yes git sudo \
 && git clone https://github.com/pyenv/pyenv.git ${PYENV_ROOT} \
 && git clone https://github.com/pyenv/pyenv-update.git ${PYENV_ROOT}/plugins/pyenv-update \
 && sudo chmod 777 ${PYENV_ROOT}

 # Install Python build dependencies (tzdata needs some special handling)
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get install --assume-yes make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm openssh-client vim \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev unzip

# Install Python 3.11.8 using pyenv
RUN apt-get -y install locales
ENV PYENV_VERSION=3.11.8
RUN /usr/local/pyenv/bin/pyenv install ${PYENV_VERSION}
RUN pyenv global ${PYENV_VERSION}
RUN pyenv rehash

# Update alternatives so that the pyenv Python is the default Python.
# We can't use an alias because the container's entrypoint is a shell script and .bashrc is not sourced.
RUN update-alternatives --install /usr/bin/python python ${PYENV_ROOT}/versions/${PYENV_VERSION}/bin/python 1

# Set working directory and copy the project files
WORKDIR /src/flask_forge
COPY pyproject.toml requirements.txt /src/flask_forge /app/

# Build the virtual environment
RUN eval "$(pyenv init -)" \
 && make venv

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the project script defined in the pyproject.toml file
RUN CMD ["run"]