#!/bin/bash

curl https://sdk.cloud.google.com > install.sh
bash install.sh --disable-prompts

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/google-cloud-sdk/bin:/root/google-cloud-sdk/bin

