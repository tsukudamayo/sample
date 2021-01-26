FROM node:buster
ENV LANG ja_JP.UTF-8

RUN mkdir -p /workspace/app

RUN apt-get update \
    && apt-get install -y software-properties-common \
    wget \
    gnupg2 \
    && wget -q http://emacs.ganneff.de/apt.key -O- | apt-key add \
    && add-apt-repository "deb http://emacs.ganneff.de/ buster main" 

RUN apt-get update \
    && apt-get -y install emacs-snapshot \
    llvm \
    clang \
    libclang-dev \
    vim \
    && git clone https://github.com/tsukudamayo/dotfiles.git \
    && cp -r ./dotfiles/linux/.emacs.d ~/ \
    && cp -r ./dotfiles/.fonts ~/

WORKDIR /workspace/app
RUN npm install -g typescript \
    tslint \
    && tslint --init
EXPOSE 3000

CMD ["/bin/bash"]
