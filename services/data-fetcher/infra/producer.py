''' KAFKA producer here '''
import logging
from confluent_kafka import Producer


# Kafka configuration
KAFKA_CONF = {
    'bootstrap.servers': 'kafka-broker:9092',  # Kafka broker address
}

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KafkaProducer:
    def __init__(self):
        self.producer = Producer(**KAFKA_CONF)

    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")
    
    def fire(self, topic, message):
        self.producer.produce(topic, value=message, on_delivery=self.delivery_report)
        self.producer.flush()
