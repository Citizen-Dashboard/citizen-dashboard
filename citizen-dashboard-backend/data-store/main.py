import logging
from infra.consumer import KafkaConsumer


logger = logging.getLogger(__name__)


def store_data(msg):
    logger.info("Storing to DB")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    consumer = KafkaConsumer("scraper-records", store_data)
    consumer.start()

if __name__ == "__main__":
    main()