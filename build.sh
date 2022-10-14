#!/usr/bin/env bash

source .env
docker build --no-cache -t pure3dapp:${dockertag} \
  --build-arg gitlocation=${gitlocation} \
  --build-arg gitbranch=${gitbranch} \
  --build-arg SECRET_FILE=${SECRET_FILE} \
  --build-arg DATA_DIR=${DATA_DIR} \
  --build-arg mysecret=${mysecret} \
  .
#docker images | grep pure3dapp
#sleep 5
#docker tag pure3dapp:${dockertag} registry.diginfra.net/vicd/pure3dapp:${dockertag}
#docker images | grep pure3dapp
#docker push registry.diginfra.net/vicd/pure3dapp:${dockertag}
#
#ssh pure3d.dev 'sudo /data/pure3dapp/restart.sh'
