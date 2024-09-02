import logging
import json
from hashlib import sha256
from infra.consumer import KafkaConsumer
from infra.sql_db import SqlDB


logger = logging.getLogger(__name__)

db_driver = SqlDB()

def store_data(msg):
    msg_json = json.loads(msg)
    msg_hash = sha256(msg.encode('utf-8')).hexdigest()

    logger.info(f"Processing message: agenda-item={msg_json['meeting_id']} size={len(msg)} hash={msg_hash}")
    try:
        db_driver.add_record(msg_json)
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