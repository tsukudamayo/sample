#!/bin/bash

export DOCKER_BUILDKIT=1

docker build -t rust-dev-arm64 -f dev.arm64.Dockerfile .

if [[ "$OSTYPE" == "darwin"* ]]; then
    xhost +$(multipass list | grep docker-vm | awk '{print $3}')
    docker run -it --rm \
        -v $(pwd):/workspace \
        -v /tmp:/tmp \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -e DISPLAY=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}'):0.0 \
        --name speed-up-your-python-with-rust \
        rust-dev-arm64 \
        /bin/bash
    xhost -$(multipass list | grep docker-vm | awk '{print $3}')
else
    xhost +local:
    docker run -it --rm \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -e DISPLAY=$DISPLAY \
        --name speed-up-your-python-with-rust \
        rust-dev-arm64 \
        /bin/bash
    xhost -local:
fi

# docker run -it --rm -e USER=$USER rust-dev /bin/bash
# XXX
# emacs -nw --user ''
