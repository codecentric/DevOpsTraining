#!/bin/sh

URL=$1
cat run-docker.json | sed 's/$environment/green/g' | sed "s/x/$URL/g" > docker-deploy.json
#curl -X POST -H 'Content-Type: application/json' -d $CONTAINER_CREATE http://docker-api-proxy.service.consul:9898/container/create


