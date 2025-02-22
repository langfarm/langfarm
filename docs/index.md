---
layout: home

hero:
  name: "Langfarm"
  text: "大模型应用可观察性"
  tagline: Tracing、Token计量、集成 Dashscope API 等。
  actions:
    - theme: brand
      text: Tracing
      link: /markdown-examples
    - theme: alt
      text: API Examples
      link: /api-examples

features:
  - title: 增强 Langfuse 数据处理能力
    details: 接收 Langfuse SDK 的事件上报。数据写入 Kafka，并且通过 Flink 任务进入流式数据湖 Paimon。
  - title: Langfarm SDK 集成 Dashscope API
    details: 友好集成 Dashscope API。提供三种方式使用 Langfuse 进行 trace 上报：1、@observe 方式；2、使用 Langchain 的 Tongyi；3、借助 OpenAI SDK
  - title: 统计报表
    details: 基本 Flink + Paimon 制作近实时 Token、Cost、Api QPS、TPM 报表
---

