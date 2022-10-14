#!/usr/bin/env bash

ssh pure3d.dev 'sudo git clone -b containerize https://github.com/CLARIAH/pure3d.git /tmp/app'
scp .env pure3d.dev:/tmp/app/
ssh pure3d.dev 'sudo ./build.sh'

