---
layout: home

hero:
  name: "Langfarm"
  text: "LLM App Observability"
  tagline: Tracing、Token Usage、Integration Dashscope API and so on。
  actions:
    - theme: brand
      text: Tracing
      link: /markdown-examples
    - theme: alt
      text: API Examples
      link: /api-examples

features:
  - title: Enhance Langfuse Data Processing Capacity
    details: Receive event reports from the Langfuse SDK. Write the data to Kafka and then process it through a Flink task to enter the streaming data lake Paimon.
  - title: Langfarm SDK Integration Dashscope API
    details: Friendly integration with Dashscope API. Langfuse offers three ways to report traces. 1. Using the @observe method; 2. Through Langchain's Tongyi; 3. With the OpenAI SDK.
  - title: Statistical report form
    details: Basic Flink + Paimon produces near-real-time Token, Cost, Api QPS, TPM reports
---

