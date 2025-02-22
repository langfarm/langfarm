# Tracing 写入数据湖

## 启动 paimon-flink

还没启动 langfarm 请看：[快速开始 Langfarm](../quick-start.md)
```bash
# 启动 paimon-flink
sh scripts/start-docker-compose-paimon-flink.sh
```

## 运行 写 Paimon 的任务
```bash
# 向 flink 群集提交两个从 kafka 到 paimon 的 flink 任务
sh scripts/submit-tracing-to-paimon-task.sh
``` 

查看提交的 flink 任务：http://localhost:8081/#/job/running

![tracing-kafka-to-paimon](/img/streaming/tracing-kafka-to-paimon.png)

## 查看数据

3 分钟后（paimon 数据提交到文件中依赖于 flink 的 checkpoint 间隔），数据会写入到 paimon 数据湖中。

进入 flink sql client
```bash
sh scripts/into-flink-sql-cli.sh
```

执行如下 sql
```sql
-- 使用 tableau 的格式展示结果
SET 'sql-client.execution.result-mode' = 'tableau';

-- 用 '批模型' 运行查询数据
SET 'execution.runtime-mode' = 'batch';

-- 查询 traces 表
select id,SPLIT_INDEX(id, '-', 4) as sid, name, REGEXP_REPLACE(input, '\n', ' ') as input, created_at, updated_at, dt, hh from langfarm.tracing.traces order by created_at desc limit 10;

-- 查询 observations 表
select id,SPLIT_INDEX(id, '-', 4) as sid, name, REGEXP_REPLACE(input, '\n', ' ') as input, created_at, updated_at, dt, hh from langfarm.tracing.observations order by created_at desc limit 10;
```

结果如下：
```console
Flink SQL> SET 'sql-client.execution.result-mode' = 'tableau';
[INFO] Execute statement succeeded.

Flink SQL> SET 'execution.runtime-mode' = 'batch';
[INFO] Execute statement succeeded.

Flink SQL> select id,SPLIT_INDEX(id, '-', 4) as sid, name, REGEXP_REPLACE(input, '\n', ' ') as input, created_at, updated_at, dt, hh from langfarm.tracing.traces order by created_at desc limit 10;
+--------------------------------+--------------+---------------------+--------------------------------+----------------------------+----------------------------+------------+----+
|                             id |          sid |                name |                          input |                 created_at |                 updated_at |         dt | hh |
+--------------------------------+--------------+---------------------+--------------------------------+----------------------------+----------------------------+------------+----+
| f9936670-b7d9-41ef-ab5b-db5... | db59cd617c24 |    RunnableSequence | 把 a = b + c 转成 json 对象... | 2024-12-12 00:07:09.474776 | 2024-12-12 00:07:11.272232 | 2024-12-12 | 00 |
| 62518226-b25f-41ef-9554-e83... | e835d41b15a9 | dashscope_hook_call |     请用50个字描写春天的景色。 | 2024-12-05 00:47:01.292087 | 2024-12-05 00:47:03.316830 | 2024-12-05 | 00 |
+--------------------------------+--------------+---------------------+--------------------------------+----------------------------+----------------------------+------------+----+
2 rows in set (3.34 seconds)

Flink SQL> select id,SPLIT_INDEX(id, '-', 4) as sid, name, REGEXP_REPLACE(input, '\n', ' ') as input, created_at, updated_at, dt, hh from langfarm.tracing.observations order by created_at desc limit 10;
+--------------------------------+--------------+----------------------+--------------------------------+----------------------------+----------------------------+------------+----+
|                             id |          sid |                 name |                          input |                 created_at |                 updated_at |         dt | hh |
+--------------------------------+--------------+----------------------+--------------------------------+----------------------------+----------------------------+------------+----+
| f9936670-b7d9-41ef-831e-147... | 147575b87fb0 |     RunnableSequence | 把 a = b + c 转成 json 对象... | 2024-12-12 00:07:09.474776 | 2024-12-12 00:07:11.272136 | 2024-12-12 | 00 |
| f9936670-b7d9-41ef-9324-a8a... | a8a6f5a0fc66 |     JsonOutputParser | ```json {   "a": {     "ope... | 2024-12-12 00:07:09.474776 | 2024-12-12 00:07:11.272022 | 2024-12-12 | 00 |
| f9936670-b7d9-41ef-a6d8-349... | 349d922503d8 |               Tongyi | 把 a = b + c 转成 json 对象... | 2024-12-12 00:07:09.474776 | 2024-12-12 00:07:11.269811 | 2024-12-12 | 00 |
| 62518226-b25f-41ef-aa47-c6c... | c6cd4b377b52 | Dashscope-generation |     请用50个字描写春天的景色。 | 2024-12-05 00:47:01.292087 | 2024-12-05 00:47:03.230789 | 2024-12-05 | 00 |
+--------------------------------+--------------+----------------------+--------------------------------+----------------------------+----------------------------+------------+----+
4 rows in set (0.92 seconds)

```