import logging
import random
from confluent_kafka import Consumer, KafkaError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

KAFKA_CONF = {
    'bootstrap.servers': 'kafka-broker:9092', 
    'group.id': f'data-store',
    'auto.offset.reset': 'earliest'
}

class KafkaConsumer:
    def __init__(self, topic, callback) -> None:
        self.consumer = Consumer(**KAFKA_CONF)
        self.consumer.subscribe([topic])
        self.callback = callback

    def start(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)  # Timeout in seconds

                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.error(f"Reached end of partition {msg.partition()} at offset {msg.offset()}")
                    else:
                        logger.error(f"Error: {msg.error()}")
                else:
                    logger.info(f"Received message: {msg.value().decode('utf-8')} from partition {msg.partition()} at offset {msg.offset()}")
                    self.callback(msg.value().decode('utf-8'))
        finally:
            self.consumer.close()
