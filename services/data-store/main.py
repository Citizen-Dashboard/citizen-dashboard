import logging
from infra.consumer import KafkaConsumer
from infra.db import SQLDB


logger = logging.getLogger(__name__)

db_driver = SQLDB()

def store_data(msg):
    logger.info(f"Storing to DB: {msg}")
    db_driver.add_record("hello", "world")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    consumer = KafkaConsumer("scraper-records", store_data)
    consumer.start()

if __name__ == "__main__":
    main()