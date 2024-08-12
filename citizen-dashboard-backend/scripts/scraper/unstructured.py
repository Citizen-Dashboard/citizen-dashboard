import requests
import pandas as pd
from bs4 import BeautifulSoup
import fastavro
import random
import time
import logging
import os
from fastavro.schema import load_schema

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_random_wait():
    wait_time = random.uniform(13, 37)  # Random wait time between 13 and 37 seconds
    logging.info(f'Waiting for {wait_time:.2f} seconds before making the next request.')
    return wait_time

def extract_h4_titles_and_content(url):
    logging.info(f'Starting to scrape URL: {url}')
    time.sleep(get_random_wait())  # Wait before making the request
    response = requests.get(url)
    if response.status_code == 200:
        logging.info(f'Successfully fetched content from URL: {url}')
    else:
        logging.error(f'Failed to fetch content from URL: {url}, Status Code: {response.status_code}')
        return []
    soup = BeautifulSoup(response.content, 'html.parser')
    titles_and_content = []
    for h4 in soup.find_all('h4'):
        title = h4.get_text(strip=True)
        if "Confidential" in title:
            continue  # Skip titles containing "Confidential"
        content = []
        for sibling in h4.find_next_siblings():
            if sibling.name == 'h4':
                break
            content.append(sibling.get_text(strip=True))
        titles_and_content.append({"title": title, "content": ' '.join(content)})
    logging.info(f'Extracted {len(titles_and_content)} titles and content from URL: {url}')
    return titles_and_content

def append_to_avro(records, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            existing_records = list(fastavro.reader(f))
            records = existing_records + records
    with open(file_path, 'wb') as avro_file:
        # Determine the schema dynamically
        schema = {
            "type": "record",
            "name": "CityCouncilRecord",
            "fields": [{"name": key, "type": "string"} for key in records[0].keys()]
        }
        fastavro.writer(avro_file, schema, records, codec='deflate')

def main():
    # Read the agenda item IDs from the combined_data.parquet file
    logging.info('Reading agenda item IDs from combined_data.parquet')
    df_combined = pd.read_parquet('data/combined_data.parquet')
    items = df_combined['Agenda Item #'].astype(str).unique()  # Ensure agenda item IDs are strings
    base_url = 'https://secure.toronto.ca/council/agenda-item.do?item='
    urls = [base_url + item for item in items]

    file_path_avro = 'data/items_info.avro'
    max_pages = 1000
    page_count = 0

    for item, url in zip(items, urls):
        if page_count >= max_pages:
            logging.info(f'Termination variable reached: {max_pages} pages scraped.')
            break

        titles_and_content = extract_h4_titles_and_content(url)
        for record in titles_and_content:
            record["agenda_item_id"] = item  # Add agenda item ID to the record

        if titles_and_content:
            logging.info('Appending new data to Avro file.')
            append_to_avro(titles_and_content, file_path_avro)

        page_count += 1

    logging.info('Web scraping process completed.')

if __name__ == "__main__":
    logging.info('Starting the web scraping process.')
    main()
    logging.info('Web scraping process completed.')
