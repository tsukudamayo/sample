#!/bin/bash

xhost +local:
docker run \
    -it --rm \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $(dirname $(pwd);):/workspace/app \
    -v /media/tsukudamayo/0CE698DCE698C6FC2/tmp/data:/workspace/data \
    -e DISPLAY=$DISPLAY \
    puppeteer-ts-dev \
    /bin/bash
xhost -local:
