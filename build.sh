#!/usr/bin/env bash

git checkout containerize
git pull
source .env
docker build --no-cache -t pure3dapp:${dockertag} \
  --build-arg gitlocation=${gitlocation} \
  --build-arg gitbranch=${gitbranch} \
  --build-arg SECRET_FILE=${SECRET_FILE} \
  --build-arg DATA_DIR=${DATA_DIR} \
  --build-arg mysecret=${mysecret} \
  .

docker tag pure3dapp:${dockertag} registry.diginfra.net/vicd/pure3dapp:${dockertag}
docker push registry.diginfra.net/vicd/pure3dapp:${dockertag}

docker-compose --env-file /data/pure3dapp/.env -f /data/pure3dapp/docker-compose-acc.yml down
docker pull registry.diginfra.net/vicd/pure3dapp:0.1
docker-compose --env-file /data/pure3dapp/.env -f /data/pure3dapp/docker-compose-acc.yml up -d

