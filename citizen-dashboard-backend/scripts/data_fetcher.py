import argparse
import logging
import pandas as pd
import os
import json
from fetch_voting_records import fetch_voting_records
from scraper.hybrid import process_items  # Ensure this import points to the correct location

MIN_WAIT = 13
MAX_WAIT = 37

VOTING_RECORD_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
MEETING_API_BASE_URL = "https://secure.toronto.ca/council/agenda-item.do?item="

PACKAGE_ID = "members-of-toronto-city-council-voting-record"
VOTING_RECORD_PATH = 'data/combined_voting_data.csv'
ITEM_DATA_PATH = 'data/items_data.csv'

AGENDA_ITEMS_LAYOUT_FILE = 'agenda_items_table_layout.json'

# Load the table layout from the JSON file
with open(AGENDA_ITEMS_LAYOUT_FILE) as f:
    table_layout = json.load(f)['columns']

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_data(base_url, package_id, local_file_path):
    # Ensure the directory exists
    directory = os.path.dirname(local_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")

    # Check if the file exists
    if os.path.exists(local_file_path):
        logger.info(f"Loading data from CSV file: {local_file_path}")
        combined_df = pd.read_csv(local_file_path)
        if combined_df.empty:
            logger.warning("Loaded data is empty. Fetching new data from the API.")
            combined_df = fetch_voting_records(base_url, package_id)
            if combined_df is not None:
                save_to_csv(combined_df, local_file_path)
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
            save_to_csv(combined_df, local_file_path)
        else:
            logger.warning("No data fetched. Exiting.")
            return None

    return combined_df

def save_to_csv(df, file_path):
    logger.info(f"Saving combined data to CSV file: {file_path}")
    df.to_csv(file_path, index=False)
    logger.info("Data saved successfully")

def main():

    combined_voting_record = fetch_data(VOTING_RECORD_URL, PACKAGE_ID, VOTING_RECORD_PATH)
    
    if combined_voting_record is not None:
        items = combined_voting_record['Agenda Item #'].astype(str).unique()

        if os.path.exists(ITEM_DATA_PATH):
            logger.info(f"Reading existing items from {ITEM_DATA_PATH}")
            df_agenda_items = pd.read_csv(ITEM_DATA_PATH)
            existing_items = df_agenda_items['item_id'].unique()
            items = [item for item in items if item not in existing_items]
        else:
            df_agenda_items = pd.DataFrame(columns=[column['name'] for column in table_layout])
            df_agenda_items.to_csv(ITEM_DATA_PATH, index=False)
            logger.info(f"Created empty CSV file: {ITEM_DATA_PATH}")

        logger.info("Starting the hybrid processing")
        process_items(items, MEETING_API_BASE_URL, ITEM_DATA_PATH, MIN_WAIT, MAX_WAIT, table_layout)
        logger.info("Hybrid processing completed")
    else:
        logger.warning("No data to process. Exiting.")

if __name__ == "__main__":
    main()