# Langfarm Quick Start

## start at docker compose

启动 langfarm 和它依赖的服务
```bash
sh scripts/start-docker-compose.sh

# 初始化 postgres data
sh scripts/init-postgres-docker-data.sh

# 启动依赖服务的 ui 界面的 docker
sh scripts/start-docker-compose-infra-ui.sh
```

## post data

### curl post

已经按 langfuse 格式生成的测试数据
```bash
# 四份测试数据
sh scripts/post-event-data.sh trace-01-part1
sh scripts/post-event-data.sh trace-01-part2
sh scripts/post-event-data.sh trace-02-part1
sh scripts/post-event-data.sh trace-02-part2
```

进入 kafka ui 查看数据 http://localhost:8080/ui/clusters/langfarm/all-topics

![kafak-ui-show-topic](/img/tracing/kafka-ui-show-topic.png)

### langfuse sdk post

TODO