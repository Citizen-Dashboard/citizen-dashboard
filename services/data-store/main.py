import logging
import json
from infra.consumer import KafkaConsumer
from infra.sql_db import SqlDB


logger = logging.getLogger(__name__)

db_driver = SqlDB()

def store_data(msg):
    try:
        db_driver.add_record(json.loads(msg))
    except Exception as e:
        logger.error(e)
    finally:
        logger.info(f"Stored to DB: {msg}")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    consumer = KafkaConsumer("scraper-records", store_data)
    consumer.start()

if __name__ == "__main__":
    main()