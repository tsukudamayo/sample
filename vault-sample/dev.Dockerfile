FROM ubuntu:20.04 

ENV HOME /home
ENV PATH $PATH:$HOME/.local/bin
ENV PYTHON_VERSION 3.11.0 
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /home

# build python
RUN apt update && apt install -y tzdata \
    sudo \
    software-properties-common \
    wget \
    curl \
    gnupg2 \
    git \
    libssl-dev \
    zlib1g-dev \
    pkg-config \
    libncurses5-dev \
    build-essential \
    gnutls-bin \
    libgdbm-dev \
    libnss3-dev \
    libreadline-dev \
    libffi-dev \
    libsqlite3-dev \
    libbz2-dev \
    # for scipy install
    # gfortran libopenblas-dev liblapack-dev \
    && wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz \
    && tar -xf Python-${PYTHON_VERSION}.tgz

WORKDIR /home/Python-${PYTHON_VERSION}
RUN ./configure --enable-optimizations \
    && make -j 8 \
    && make install \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt install -y nodejs \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && pip3 install python-lsp-server pyright \
    && ln -sf /usr/local/bin/python3 /usr/local/bin/python \
    && ln -sf /usr/local/bin/pip3 /usr/local/bin/pip \
    && rm -rf /home/Python-${PYTHON_VERSION} \
    && rm /home/Python-${PYTHON_VERSION}.tgz

WORKDIR /workspace

RUN apt update && apt install -y gpg \
    && wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg \
    && gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list \
    && curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add - \
    && apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
    && apt update && apt install -y consul \
    vault \
    && setcap -r /usr/bin/vault \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["/bin/bash"]
