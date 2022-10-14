#!/usr/bin/env bash

ssh pure3d.dev 'sudo git clone -b https://github.com/CLARIAH/pure3d.git containerize /tmp/app && cd /tmp/app && sudo ./build.sh'
