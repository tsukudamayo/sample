#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
    xhost +localhost
    docker run -it --rm \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -v $(pwd):/workspace \
        atcoder-dev \
        /bin/bash
    xhost -localhost
else
    xhost +local:
    docker run -it --rm \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -v $(pwd):/workspace \
        -e DISPLAY=$DISPLAY \
        atcoder-dev \
        /bin/bash
    xhost -local:
fi
