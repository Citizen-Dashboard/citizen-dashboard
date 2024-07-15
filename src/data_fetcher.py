import logging
import requests
import pandas as pd
import io
import os

logger = logging.getLogger(__name__)

def fetch_data(base_url, package_id, from_local=False, local_file_path='combined_data.parquet'):
    if from_local and os.path.exists(local_file_path):
        logger.info(f"Loading data from Parquet file: {local_file_path}")
        combined_df = pd.read_parquet(local_file_path)
        logger.info("Data loaded successfully")
        return combined_df

    logger.info("Fetching package metadata...")
    package_url = f"{base_url}/api/3/action/package_show"
    params = {"id": package_id}
    package_response = requests.get(package_url, params=params)
    package_data = package_response.json()

    if not package_data['success']:
        logger.error("Failed to fetch package metadata")
        raise Exception("Failed to fetch package metadata")
    logger.info("Package metadata fetched successfully")

    dataframes = []

    for resource in package_data["result"]["resources"]:
        if resource["datastore_active"]:
            logger.info(f"Fetching data for resource: {resource['name']}")
            csv_url = f"{base_url}/datastore/dump/{resource['id']}"
            csv_data = requests.get(csv_url).text
            
            try:
                df = pd.read_csv(io.StringIO(csv_data))
                dataframes.append(df)
                logger.info(f"Data fetched and converted to DataFrame for resource: {resource['name']}")
            except pd.errors.ParserError as e:
                logger.warning(f"Error parsing {resource['name']}: {e}")
            except Exception as e:
                logger.warning(f"An error occurred while processing {resource['name']}: {e}")

    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        logger.info("Combined all DataFrames into one")
        logger.info(f"Combined DataFrame shape: {combined_df.shape}")
        
        # Save the combined DataFrame to a Parquet file
        save_to_parquet(combined_df, local_file_path)
        
        return combined_df
    else:
        logger.warning("No datastore active resources found")
        return None

def save_to_parquet(df, file_path):
    logger.info(f"Saving combined data to Parquet file: {file_path}")
    df.to_parquet(file_path, compression='snappy')
    logger.info("Data saved successfully")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    package_id = "members-of-toronto-city-council-voting-record"
    dataframes = fetch_data(base_url, package_id)
    print(f"Number of DataFrames fetched: {len(dataframes)}")