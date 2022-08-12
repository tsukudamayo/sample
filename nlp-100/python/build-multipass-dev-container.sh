#!/bin/bash

export DOCKER_BUILDKIT=1

docker build -t python311-dev -f dev.multipass.Dockerfile .

if [[ "$OSTYPE" == "darwin"* ]]; then
    xhost +$(multipass list | grep docker-vm | awk '{print $3}')
    docker run -it --rm \
        -v $(pwd):/workspace:delegated \
        -v /tmp/.X11-unix:/tmp/.X11-unix:delegated \
        -e DISPLAY=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}'):0.0 \
        --name nlp-100-python \
        python311-dev \
        /bin/bash
    xhost -$(multipass list | grep docker-vm | awk '{print $3}')

else
    xhost +local:
    docker run -it --rm \
        -v $HOME:$HOME \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -e DISPLAY=$DISPLAY \
        --name nlp-100-python \1
        python311-dev \
        /bin/bash
    xhost -local:
fi
