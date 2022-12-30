FROM rust:slim-bullseye

ENV HOME /home
ENV PATH $PATH:$HOME/.cargo/bin

WORKDIR /home

RUN apt-get update \
    && apt-get install -y software-properties-common \
    wget \
    curl \
    gnupg2 \
    git \
    libssl-dev \
    pkg-config \
    build-essential \
    gnutls-bin \
#     llvm \
#     clang \
#     libclang-dev \
#     lldb \
#     gdb \
    && rustup update \
    && rustup component add rustfmt clippy rls rust-analysis rust-src  \
    && mkdir -p ~/.cargo/bin \
    && curl -L https://github.com/rust-analyzer/rust-analyzer/releases/latest/download/rust-analyzer-x86_64-unknown-linux-gnu.gz | gunzip -c - > ~/.cargo/bin/rust-analyzer \
    && chmod +x ~/.cargo/bin/rust-analyzer \ 
    && cargo install cargo-edit \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

CMD ["/bin/bash"]
