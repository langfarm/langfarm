import json
import logging

from confluent_kafka import Consumer
from langfarm_tests.base_for_test import get_test_logger
from langfarm_tracing.kafka import KafkaMessage, headers_to_dict

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
