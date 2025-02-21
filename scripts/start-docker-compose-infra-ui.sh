#!/bin/sh

docker compose -f docker/docker-compose-infra-ui.yml -p langfarm-infra-ui up -d
