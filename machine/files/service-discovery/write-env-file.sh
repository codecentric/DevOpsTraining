#!/usr/bin/env bash

until [ "`/usr/bin/docker inspect -f {{.State.Running}} consul`" == "true" ]; do
    sleep 0.1;
done;

JOIN_IP=$(docker inspect -f '{{.NetworkSettings.Networks.servicediscovery_default.IPAddress}}' consul)
echo "CONCOURSE_GARDEN_DNS_SERVER=$JOIN_IP" > /opt/service-discovery/environment