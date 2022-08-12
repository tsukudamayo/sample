#!/bin/bash

export DOCKER_BUILDKIT=1

docker build -t rust-dev -f dev.Dockerfile .

if [[ "$OSTYPE" == "darwin"* ]]; then
    xhost +$(multipass list | grep docker-vm | awk '{print $3}')
    docker run -it --rm \
        -v $(pwd):/workspace \
        -v /tmp:/tmp \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -e DISPLAY=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}'):0.0 \
        --name nlp-100-rust \
        rust-dev \
        /bin/bash
    xhost -$(multipass list | grep docker-vm | awk '{print $3}')
else
    xhost +local:
    docker run -it --rm \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -e DISPLAY=$DISPLAY \
        --name atcoder-rust \
        atcoder-rust \
        /bin/bash
    xhost -local:
fi

# docker run -it --rm -e USER=$USER rust-dev /bin/bash
# XXX
# emacs -nw --user ''
