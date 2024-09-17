import os
from random import choice
from confluent_kafka import Producer
from kafka.kafka_admin import Kafa_Admin
import asyncio
import json
from app_logging.logger import File_Console_Logger


logger = File_Console_Logger(__name__)


class kafka_producer:
    """
    A Kafka producer class for sending messages to a specified topic.

    This class provides functionality to configure a Kafka producer,
    produce messages to a specified topic, and handle message delivery.
    It uses the confluent_kafka library and integrates with a custom
    logging system.

    Attributes:
        producer (confluent_kafka.Producer): The Kafka producer instance.
        topic (str): The Kafka topic to produce messages to.
        topic_ready (bool): Indicates whether the topic is ready for use.

    Methods:
        __init__(topic): Initializes the Kafka producer with the specified topic.
        delivery_callback(err, msg): Callback function for message delivery status.
        produce(message, id): Produces a message to the Kafka topic.
        flush(): Flushes the producer to ensure all messages are sent.
    """

    def __init__(self, topic):
        """
        Initializes the Kafka producer with the specified topic.

        This method sets up the Kafka producer configuration, creates the producer instance,
        and checks if the specified topic is ready for use.

        Args:
            topic (str): The Kafka topic to produce messages to.

        Attributes:
            producer (confluent_kafka.Producer): The Kafka producer instance.
            topic (str): The Kafka topic to produce messages to.
            topic_ready (bool): Indicates whether the topic is ready for use.

        Raises:
            None, but logs errors if there are issues with topic creation or readiness.

        Note:
            The method uses environment variables for configuration, specifically
            'Plaintext_Ports' for the Kafka broker port.
        """
        logger.info(f'configuring port : {os.environ.get("Plaintext_Ports")}')
        config = {
            # User-specific properties that you must set
            'bootstrap.servers': f'localhost:{os.environ.get("Plaintext_Ports")}',

            # Fixed properties
            'acks': 'all'
        }
            
        # Create Producer instance
        self.producer = Producer(config)
        self.topic = topic
        self.topic_ready = Kafa_Admin.check_create_topic(topic)



    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(self, err, msg):
        """
        Callback function for message delivery status.

        This method is called when a message has been successfully delivered or
        permanently failed delivery (after retries). It logs the delivery status
        and provides feedback on the message's success or failure.

        Args:
            err (Exception): The error object if delivery failed, otherwise None.
            msg (confluent_kafka.Message): The message object.

        Returns:
            None
        """
        if err:
            logger.error('Message failed delivery: {}'.format(err))
        else:
            logger.info("Produced event to topic {topic}: key = {key:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8')))



    def produce(self,message, id):
        """
        Produces a message to the Kafka topic.

        This method produces a message to the specified Kafka topic. It checks if the topic is ready
        and then produces the message with the given key. The message is serialized to JSON and sent
        as a UTF-8 encoded string.

        Args:
            message (dict): The message to be produced.
            id (str): The key for the message.

        Returns:
            bool: True if the message was produced successfully, False otherwise.
        """
        
        if not self.topic_ready:
            self.delivery_callback(Exception("Topic is not ready"), "Topic not ready")
            return False
        
        # Produce data by selecting random values from these lists.
        self.producer.produce(self.topic, json.dumps(message).encode("utf-8"), id, callback=self.delivery_callback)
        logger.debug(f"Produced event to topic {self.topic}: key = {id}")
    
    async def flush(self):
        # Block until the messages are sent.
        await asyncio.get_event_loop().run_in_executor(None, self.producer.flush, 1000)
