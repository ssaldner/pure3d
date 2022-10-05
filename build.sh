#!/usr/bin/env bash

source .env
docker build -t pure3dapp:${gittag} \
  --build-arg gitlocation=${gitlocation} \
  --build-arg gitbranch=${gitbranch} \
  --build-arg SECRET_FILE=${SECRET_FILE} \
  --build-arg DATA_DIR=${DATA_DIR} \
  --build-arg mysecret=${mysecret} \
  .
