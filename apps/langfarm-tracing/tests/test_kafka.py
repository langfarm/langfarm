import json
import logging
import unittest

from confluent_kafka import Producer, Consumer
from testcontainers.core.container import DockerContainer
from testcontainers.kafka import KafkaContainer

from langfarm_tests.base_container import BaseContainerTestCase
from langfarm_tests.base_for_test import get_test_logger, read_file_to_dict
from langfarm_tracing.config import KafkaConfig

from langfarm_tracing.kafka import KafkaMessage, headers_to_dict, get_kafka_producer, KafkaSink

logger = get_test_logger(__name__)


class KafkaSource:
    def __init__(self, bootstrap_server: str, topic: str, group_id: str, offset_reset: str = "earliest"):
        """
        kafka 消息消费
        :param topic: 主题
        :param group_id: 消耗组 id
        :param offset_reset: 'earliest' or 'latest'。默认 'earliest'
        """
        receive_config = {
            "bootstrap.servers": bootstrap_server,
            "group.id": group_id,
            "auto.offset.reset": offset_reset,
        }

        self.receive_config = receive_config
        self.topic = topic
        self.group_id = group_id

        logger.info("receive_config = %s", receive_config)

        consumer = Consumer(receive_config)
        consumer.subscribe([topic])
        self.consumer = consumer

    def poll_message(self, timeout) -> KafkaMessage | None:
        msg = self.consumer.poll(timeout)
        if msg is None:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(
                    "poll message is null within timeout = %s, receive_config = %s", timeout, self.receive_config
                )
            return None
        elif msg.error():
            logger.error("receive_message_error: %s", msg.error())
            return None
        else:
            key = msg.key().decode("utf-8")
            message = json.loads(msg.value().decode("utf-8"))
            header = headers_to_dict(msg.headers())

            return KafkaMessage(key, message, header)

    def close(self):
        self.consumer.close()
        logger.info("Consumer close! topic = %s, group_id = %s", self.topic, self.group_id)


class KafkaContainerTestCase(BaseContainerTestCase):
    kafka_container: KafkaContainer
    bootstrap_server: str
    producer: Producer
    kafka_sink: KafkaSink
    kafka_source: KafkaSource

    @classmethod
    def _init_docker_container(cls) -> DockerContainer:
        cls.kafka_container = KafkaContainer()
        return cls.kafka_container

    @classmethod
    def _set_up_class_other(cls):
        cls.bootstrap_server = cls.kafka_container.get_bootstrap_server()
        cls.producer = get_kafka_producer(KafkaConfig(KAFKA_BOOTSTRAP_SERVERS=cls.bootstrap_server))
        topic = "test_tracing_topic"
        cls.kafka_sink = KafkaSink(cls.producer, topic)
        cls.kafka_source = KafkaSource(cls.bootstrap_server, topic, "test_tracing_group")

    @classmethod
    def _tear_down_class_other(cls):
        if cls.kafka_source:
            cls.kafka_source.close()

    def setUp(self):
        logger.info("")

    def test_kafka_send_message(self):
        events_dict = read_file_to_dict(__file__, "mock-data/trace-01-part1.json")
        metadata = events_dict["metadata"]
        logger.info("metadata=%s", metadata)
        for event in events_dict["batch"]:
            logger.info("event=%s", event)
            self.kafka_sink.send_trace_ingestion(event["id"], event, metadata)
            self.kafka_sink.flush(5)

        # 验证 kafka 的发送
        for event in events_dict["batch"]:
            msg = self.kafka_source.poll_message(timeout=10)
            logger.info("rev=%s", msg)
            assert msg
            assert msg.key == event["id"]
            assert msg.body == event
            assert msg.header["batch_size"] == str(metadata["batch_size"])
            assert msg.header["sdk_version"] == str(metadata["sdk_version"])


if __name__ == "__main__":
    unittest.main()
