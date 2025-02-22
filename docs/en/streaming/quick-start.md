# Tracing Write Into Lakehouse

start paimon-flink docker-compose
```bash
sh scripts/start-docker-compose-paimon-flink.sh
```

submit tracing to paimon task
```bash
# 向 flink 群集提交两个从 kafka 到 paimon 的 flink 任务
sh scripts/submit-tracing-to-paimon-task.sh
``` 

see flink that task：http://localhost:8081/#/job/running

![tracing-kafka-to-paimon](/img/streaming/tracing-kafka-to-paimon.png)
