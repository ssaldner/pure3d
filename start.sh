#!/usr/bin/env bash

ssh pure3d.dev 'sudo git clone -b containerize https://github.com/CLARIAH/pure3d.git /tmp/app && cd /tmp/app && sudo ./build.sh'
