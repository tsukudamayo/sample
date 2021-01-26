#!/bin/bash

docker run \
    -it --rm \
    -v $(dirname $(pwd);):/workspace/app \
    -v /media/tsukudamayo/0CE698DCE698C6FC2/tmp/data:/workspace/data \
    -e DISPLAY=$DISPLAY \
    ts-dev \
    /bin/bash
