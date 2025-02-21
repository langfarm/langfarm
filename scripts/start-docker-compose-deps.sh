#!/bin/sh

docker compose -f docker/docker-compose-deps.yml -p langfarm up -d --remove-orphans
