#!/usr/bin/env bash

source .env
ssh pure3d.dev 'sudo git clone -b ${gitbranch} ${gitlocation} /tmp/app && cd /tmp/app && sudo ./build.sh'
