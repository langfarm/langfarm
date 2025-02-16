import unittest

from container_for_test import TracingKafkaContainerAware
from kafka_for_test import KafkaSource
from langfarm_tests.base_container import (
    DockerComposeTestCase,
    DockerContainerFactory,
    KafkaContainerFactory,
)
from langfarm_tests.base_for_test import get_test_logger, read_file_to_dict

from langfarm_tracing.kafka import KafkaSink

logger = get_test_logger(__name__)


class KafkaContainerTestCase(DockerComposeTestCase, TracingKafkaContainerAware):
    kafka_sink: KafkaSink
    kafka_source: KafkaSource

    @classmethod
    def create_docker_factory_list(cls) -> list[DockerContainerFactory]:
        cls.kafka_container_factory = KafkaContainerFactory()
        return [cls.kafka_container_factory]

    @classmethod
    def after_docker_compose_started(cls):
        cls.init_kafka_producer()
        topic = "test_tracing_topic"
        cls.kafka_sink = KafkaSink(cls.producer, topic)
        cls.kafka_source = KafkaSource(cls.bootstrap_server, topic, "test_tracing_group")

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
