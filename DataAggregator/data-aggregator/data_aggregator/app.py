# Load environment variables before importing anything else
import os
from dotenv import load_dotenv
load_dotenv()

print("*** ",os.environ.get("log_level"))

from datetime import datetime, timedelta
import asyncio

from agendaItemFetcher import adgendaItemFetcher
from kafka.kafka_producer import kafka_producer

from app_logging.logger import File_Console_Logger

logger = File_Console_Logger(__name__)



async def main():
    # check if env variables are set
    if os.environ.get("Kafka_REST_Port") is None:
        logger.error("Kafka_REST_Port is not set")
        exit(1)
    if os.environ.get("kafka_agendaItem_topic") is None:
        logger.error("kafka_agendaItem_topic is not set")
        exit(1)
        
    itemFetcher = adgendaItemFetcher()
    startDate = datetime.today() - timedelta(days=int(os.environ.get("Fetch_from_Past_nth_day")))
    endDate = datetime.today() - timedelta(days=int(os.environ.get("Fetch_to_Past_nth_day")))
    
    agendaItemsJSON = itemFetcher.getAgendaItems(startDate, endDate)
    logger.debug(agendaItemsJSON)

    agendaItem_kafka_producer = kafka_producer(topic=os.environ.get("kafka_agendaItem_topic"))
    totalItems = len(agendaItemsJSON)
    # random_item = random.choice(agendaItemsJSON)
    logger.info(f'Total agenda items: {totalItems}')
    # print(f'Random agenda item: {random_item}')
    for item in agendaItemsJSON:
        agendaItem_kafka_producer.produce( message=item, id=item.get("id"))
    # agendaItem_kafka_producer.produce(message=random_item, id=random_item.get("id"))
    
    await agendaItem_kafka_producer.flush()



if __name__ == "__main__":
    asyncio.run(main())
