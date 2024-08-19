import argparse
import logging
import pandas as pd
import os
from fetch_voting_records import fetch_voting_records
from hybrid import process_items  # Ensure this import points to the correct location

MIN_WAIT = 3
MAX_WAIT = 5

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

def fetch_data(base_url, package_id, local_file_path):
    # Ensure the directory exists
    directory = os.path.dirname(local_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")

    # Check if the file exists
    if os.path.exists(local_file_path):
        logger.info(f"Loading data from Parquet file: {local_file_path}")
        combined_df = pd.read_parquet(local_file_path)
        if combined_df.empty:
            logger.warning("Loaded data is empty. Fetching new data from the API.")
            combined_df = fetch_voting_records(base_url, package_id)
            if combined_df is not None:
                save_to_parquet(combined_df, local_file_path)
            else:
                logger.warning("No data fetched. Exiting.")
                return None
        else:
            logger.info("Data loaded successfully")
            return combined_df
    else:
        logger.info(f"File {local_file_path} does not exist. Fetching data from the API.")
        combined_df = fetch_voting_records(base_url, package_id)
        if combined_df is not None:
            save_to_parquet(combined_df, local_file_path)
        else:
            logger.warning("No data fetched. Exiting.")
            return None

    return combined_df

def save_to_parquet(df, file_path):
    logger.info(f"Saving combined data to Parquet file: {file_path}")
    df.to_parquet(file_path, compression='snappy')
    logger.info("Data saved successfully")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    combined_df = fetch_data(VOTING_RECORD_URL, PACKAGE_ID, VOTING_RECORD_PATH)
    
    if combined_df is not None:
        items = combined_df['Agenda Item #'].astype(str).unique()

        if os.path.exists(ITEM_DATA_PATH):
            logger.info(f"Reading existing items from {ITEM_DATA_PATH}")
            df_items_info = pd.read_parquet(ITEM_DATA_PATH)
            existing_items = df_items_info['meeting_id'].unique()
            items = [item for item in items if item not in existing_items]
        else:
            df_items_info = pd.DataFrame(columns=['meeting_id'] + COMMON_COLUMNS + ['Other'])
            df_items_info.to_parquet(ITEM_DATA_PATH)
            logger.info(f"Created empty Parquet file: {ITEM_DATA_PATH}")

        logger.info("Starting the hybrid processing")
        process_items(items, MEETING_API_BASE_URL, ITEM_DATA_PATH, MIN_WAIT, MAX_WAIT, COMMON_COLUMNS)
        logger.info("Hybrid processing completed")
    else:
        logger.warning("No data to process. Exiting.")

if __name__ == "__main__":
    print("hello")
    main()