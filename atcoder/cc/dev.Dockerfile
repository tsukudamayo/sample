FROM debian:bullseye as base
RUN apt-get update \
    && apt-get install -y wget \
    llvm \
    clang \
    libclang-dev \
    make \
    libssl-dev \
    git

FROM base as install-emacs
RUN apt-get install -y software-properties-common \
    gnupg2
RUN wget -q http://emacs.ganneff.de/apt.key -O- | apt-key add
RUN add-apt-repository "deb http://emacs.ganneff.de/ buster main"
RUN apt-get update \
    && apt-get install -y emacs-snapshot

FROM install-emacs as fetch-dotfiles
RUN git clone https://github.com/tsukudamayo/dotfiles.git \
    && cp -r ./dotfiles/linux/.emacs.d ~/ \
    && cp -r ./dotfiles/.fonts ~/ 


FROM fetch-dotfiles as build-cmake
RUN mkdir -p /workspace
WORKDIR /workspace
RUN wget https://github.com/Kitware/CMake/releases/download/v3.16.1/cmake-3.16.1.tar.gz \ 
    && tar xvf cmake-3.16.1.tar.gz \
    && rm cmake-3.16.1.tar.gz
WORKDIR /workspace/cmake-3.16.1
RUN ./bootstrap && make -j4 && make install

WORKDIR /workspace

CMD ["bin/bash"]
