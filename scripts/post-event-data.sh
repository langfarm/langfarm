#!/bin/bash

#set -e
file_name="trace-01-part1"
# 仅用于本地 docker-compose-dev.yml 测试。
a="cGstbGYtYTgyYzIzMDQtYzhlZS00YjI0LWFhZmMtZjNkMjI4Y2EzMzZjOnNrLWxmLWY2OWM2OTUxLTM0NjItNDk5Ny1iYTIyLTFjNTk4ZTgzMDhhYQ=="

if [ $# -gt 0 ] ; then
  file_name=$1
fi

curl -X POST http://localhost:3080/api/public/ingestion \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic ${a}" \
  -d "@apps/langfarm-tracing/tests/mock-data/${file_name}.json"
