#!/usr/bin/env bash

docker pull registry.diginfra.net/vicd/pure3dapp:0.1
docker-compose --env-file /data/pure3dapp/.env -f /data/pure3dapp/docker-compose-acc.yml down
sleep 1
docker-compose --env-file /data/pure3dapp/.env -f /data/pure3dapp/docker-compose-acc.yml up -d
