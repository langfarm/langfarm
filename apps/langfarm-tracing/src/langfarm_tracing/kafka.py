import decimal
import json
import logging

from confluent_kafka import Producer

from langfarm_tracing.config import KafkaConfig

logger = logging.getLogger(__name__)


def get_kafka_producer(kafka_config: KafkaConfig) -> Producer:
    logger.info("KAFKA_BOOTSTRAP_SERVERS=%s", kafka_config.KAFKA_BOOTSTRAP_SERVERS)
    kafka_producer_config = {
        # User-specific properties that you must set
        "bootstrap.servers": kafka_config.KAFKA_BOOTSTRAP_SERVERS,
        "acks": "all",
    }
    return Producer(kafka_producer_config)


def delivery_callback(err, msg):
    if err:
        logger.error("ERROR: Message failed delivery: %s", err)
    elif logger.isEnabledFor(logging.DEBUG):
        topic = msg.topic()
        key = msg.key().decode("utf-8")
        # value = msg.value().decode('utf-8')
        logger.debug("send event to topic [%s]: key = %s", topic, key)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super().default(o)


class KafkaSink:
    def __init__(self, producer: Producer, topic: str):
        """
        :param producer:
        :param topic:
        """
        self.producer = producer
        self.topic = topic

    def to_headers(self, header: dict) -> list[tuple]:
        headers: list[tuple] = []
        for k, v in header.items():
            headers.append((k, bytes(str(v), encoding="UTF-8")))

        return headers

    def send_trace_ingestion(self, key: str, data: dict, header: dict):
        headers = self.to_headers(header)
        post_data = json.dumps(data, ensure_ascii=False, cls=DecimalEncoder)
        self.producer.produce(topic=self.topic, key=key, value=post_data, headers=headers, callback=delivery_callback)

    def flush(self, timeout: float):
        self.producer.flush(timeout)


def headers_to_dict(headers: list) -> dict:
    header_map = {}
    for h in headers:
        header_map[h[0]] = h[1].decode("utf-8")

    return header_map


class KafkaMessage:
    def __init__(self, key: str, body: dict, header: dict):
        self.key = key
        self.body = body
        self.header = header

    def __str__(self):
        return str({"key": self.key, "body": self.body, "header": self.header})
