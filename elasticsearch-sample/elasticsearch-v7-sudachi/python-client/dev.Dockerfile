FROM python:3.10-slim-bullseye

ENV DISPLAY=host.docker.internal:0.0
ENV PATH $PATH:/root/.poetry/bin

RUN apt-get update && apt-get install -y \
    git \
    gcc \
    g++ \
    curl

RUN apt update && apt install -y curl \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt install -y nodejs

RUN pip install python-lsp-server pyright poetry

WORKDIR /workspace

CMD ["/bin/bash"]
