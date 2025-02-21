#!/bin/sh

# sh scripts/start-docker-compose-dev.sh
# 先启动 docker-compose-dev.yml 后 langfarm-langfuse-1 会初始化 langfuse 相关表结构。
# 体验 langfarm-tracing，需要初始化本示例的数据。仅用于本地 docker compose 环境的测试。
docker exec langfarm-postgres-1 psql -U postgres -w postgres -f /init_data.sql
