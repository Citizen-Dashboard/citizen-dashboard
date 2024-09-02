# scripts/fetch_voting_records.py

import logging
import requests
import pandas as pd
import io

logger = logging.getLogger(__name__)
VOTING_RECORD_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
PACKAGE_ID = "members-of-toronto-city-council-voting-record"

def fetch_voting_records(base_url, package_id):
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
        return combined_df
    else:
        logger.warning("No datastore active resources found")
        return None
    
if __name__ == '__main__':
    fetch_voting_records(VOTING_RECORD_URL, PACKAGE_ID)
