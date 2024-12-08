import os
from confluent_kafka import Consumer, KafkaError
from kafka.kafka_admin import Kafa_Admin
import asyncio

from app_logging.logger import File_Console_Logger

logger = File_Console_Logger(__name__)

class kafka_consumer:
    def __init__(self, topic):
        logger.debug(f'Configuring consumer on port: {os.environ.get("Plaintext_Ports")}')
        config = {
            'bootstrap.servers': f'localhost:{os.environ.get("Plaintext_Ports")}',
            'group.id': os.environ.get("kafka_agendaItem_group"),
            'auto.offset.reset': 'earliest'
        }

        # Create Consumer instance
        self.consumer = Consumer(config)
        self.topic = topic
        self.topic_ready = Kafa_Admin.topic_exists(topic)

    def subscribe(self):
        if not self.topic_ready:
            logger.error(f"ERROR: Topic {self.topic} is not ready")
            return False
        
        self.consumer.subscribe([self.topic])
        logger.debug(f"Subscribed to topic: {self.topic}")
        return True

    async def consume(self):
        if not self.topic_ready:
            logger.error(f"Topic {self.topic} is not ready")
            return

        try:
            while True:
                msg = await asyncio.get_event_loop().run_in_executor(None, self.consumer.poll, 1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.debug(f"Reached end of partition for topic {msg.topic()} [{msg.partition()}]")
                    else:
                        logger.error(f"Error while consuming message: {msg.error()}")
                else:
                    logger.info(f"Consumed event from topic {msg.topic()}: key = {msg.key().decode('utf-8') if msg.key() else 'None'}")
                    yield msg.value().decode('utf-8')
        finally:
            self.consumer.close()

    def close(self):
        self.consumer.close()
