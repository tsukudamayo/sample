FROM python:3.11-rc-slim-bullseye

ENV PATH $PATH:/root/.poetry/bin

RUN apt update && apt install -y \
    git \
    curl \
    gcc \
    g++ \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt install -y nodejs \ 
    && pip install python-lsp-server pyright \
    && echo 'export DISPLAY="$(ifconfig en0 | grep inet | grep -v inet6 | awk '{print $2}')"' \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

CMD ["/bin/bash"]
