import logging
from src.fetcher import fetch_data
from src.processor import process_items
import time

VOTING_RECORD_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
MEETING_API_BASE_URL = "https://secure.toronto.ca/council/agenda-item.do?item="

PACKAGE_ID = "members-of-toronto-city-council-voting-record"
COMMON_COLUMNS = [
    'Vote', 
    'Motions', 
    'Background Information',
    'Decision', 
    'Rulings',
    'Communications', 
    'Speakers', 
    'Origin', 
    'Summary', 
    'Recommendations'
]
VOTING_RECORD_PATH = 'data/combined_voting_data.parquet'
ITEM_DATA_PATH = 'data/items_data.parquet'

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    combined_df = fetch_data(VOTING_RECORD_URL, PACKAGE_ID)
   
    if combined_df is not None:
        items = combined_df['Agenda Item #'].astype(str).unique()

        logger.info("Starting the hybrid processing")
        process_items(items, MEETING_API_BASE_URL, ITEM_DATA_PATH, COMMON_COLUMNS)
        logger.info("Hybrid processing completed")
    else:
        logger.warning("No data to process. Exiting.")

if __name__ == "__main__":
    # time.sleep(1000)
    main()