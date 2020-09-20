# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.134.1/containers/codespaces-linux/.devcontainer/Dockerfile
FROM mcr.microsoft.com/vscode/devcontainers/universal:0-linux

USER root

# ** [Optional] Uncomment this section to install additional packages. **
RUN apt-get update --fix-missing -qy \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qy install --no-install-recommends curl wget zip unzip pv

USER codespace

RUN echo ">>> set python3 as default python <<<" \
    && sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1 \
    && sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.5 2 \
    && sudo update-alternatives --install /usr/bin/python python /opt/python/3.8/bin/python 3 \
    && python --version