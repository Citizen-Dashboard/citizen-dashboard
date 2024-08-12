import logging
import pandas as pd
import os
from fetch_voting_records import fetch_voting_records  # Ensure this import points to the correct location
from scraper import hybrid  # Ensure this import points to the correct location of hybrid.py

logger = logging.getLogger(__name__)

def fetch_data(base_url, package_id, local_file_path='data/combined_voting_data.parquet'):
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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levellevelname)s - %(message)s')
    base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    package_id = "members-of-toronto-city-council-voting-record"
    combined_df = fetch_data(base_url, package_id)
    
    if combined_df is not None:
        logger.info("Starting the hybrid processing")
        hybrid.main()
        logger.info("Hybrid processing completed")
    else:
        logger.warning("No data to process. Exiting.")
