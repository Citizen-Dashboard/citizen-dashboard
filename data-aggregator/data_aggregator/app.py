# Load environment variables before importing anything else
import os
from dotenv import load_dotenv
load_dotenv()

print("*** ",os.environ.get("log_level"))

from gen_ai.summarizer import Summaizer
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
    
    # generating summaries
    agendaItem_kafka_producer = kafka_producer(topic=os.environ.get("kafka_agendaItem_topic"))
    totalItems = len(agendaItemsJSON)

    summarizer = Summaizer()
    logger.info(f'Summarizing and pushing to kafka for {totalItems} agenda items')
    
    # random_item = random.choice(agendaItemsJSON)
    # print(f'Random agenda item: {random_item}')
    # agendaItem_kafka_producer.produce(message=random_item, id=random_item.get("id"))
    
    for item in agendaItemsJSON:
        # Combine title and summary for better context
        text_to_summarize = f"{item.get('agendaItemTitle', '')} {item.get('agendaItemSummary', '')}"
        try:
            summary_result = summarizer.summarizeTextContent(text_to_summarize)
            item['ai_summary'] = summary_result.get('summary')
            logger.debug(f"Generated summary for agenda item {item.get('id')}: {item.get('ai_summary')}")
            agendaItem_kafka_producer.produce( message=item, id=item.get("id"))
        except Exception as e:
            logger.error(f"Failed to produce agenda item {item.get('id')}: {str(e)}")
    
    logger.info('Finished generating summaries')
    
    await agendaItem_kafka_producer.flush()



if __name__ == "__main__":
    asyncio.run(main())
