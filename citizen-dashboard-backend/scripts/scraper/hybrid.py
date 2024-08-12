import requests
from bs4 import BeautifulSoup
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import random
import time
import logging
import os
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define common columns
COMMON_COLUMNS = [
    'Vote', 'Motions', 'Background Information', 'Decision', 'Rulings',
    'Communications', 'Speakers', 'Origin', 'Summary', 'Recommendations'
]

def get_random_wait():
    """Generate a random wait time."""
    wait_time = random.uniform(13, 37)
    logging.info(f'Waiting for {wait_time:.2f} seconds before making the next request.')
    return wait_time

def fetch_url_content(url):
    """Fetch the content of a URL."""
    logging.info(f'Starting to scrape URL: {url}')
    time.sleep(get_random_wait())
    response = requests.get(url)
    if response.status_code == 200:
        logging.info(f'Successfully fetched content from URL: {url}')
        return response.content
    else:
        logging.error(f'Failed to fetch content from URL: {url}, Status Code: {response.status_code}')
        return None

def parse_html(content):
    """Parse HTML content to extract titles and content."""
    soup = BeautifulSoup(content, 'html.parser')
    titles_and_content = []
    for h4 in soup.find_all('h4'):
        title = h4.get_text(strip=True)
        if "Confidential" in title:
            continue
        content = extract_content(h4)
        titles_and_content.append({"title": title, "content": content})
    logging.info(f'Extracted {len(titles_and_content)} titles and content')
    return titles_and_content

def extract_content(h4_tag):
    """Extract content following an h4 tag."""
    content = []
    for sibling in h4_tag.find_next_siblings():
        if sibling.name == 'h4':
            break
        content.append(sibling.get_text(strip=True))
    return ' '.join(content)

def categorize_title(title):
    """Categorize a title based on common columns."""
    for column in COMMON_COLUMNS:
        if column in title:
            extra_info = title.replace(column, '').strip(' ()')
            return column, extra_info if extra_info else 'default'
    return 'Other', title

def transform_records(records, meeting_id):
    """Transform records into a hybrid format."""
    hybrid_record = {"meeting_id": meeting_id}
    for record in records:
        title, key = categorize_title(record['title'])
        add_content_to_record(hybrid_record, title, key, record['content'])
    convert_dicts_to_json(hybrid_record)
    return [hybrid_record]

def add_content_to_record(hybrid_record, title, key, content):
    """Add content to the hybrid record."""
    if title in COMMON_COLUMNS:
        if title not in hybrid_record:
            hybrid_record[title] = {}
        if key in hybrid_record[title]:
            hybrid_record[title][key] += ' ' + content
        else:
            hybrid_record[title][key] = content
    else:
        if 'Other' not in hybrid_record:
            hybrid_record['Other'] = {}
        if key in hybrid_record['Other']:
            hybrid_record['Other'][key] += ' ' + content
        else:
            hybrid_record['Other'][key] = content

def convert_dicts_to_json(hybrid_record):
    """Convert dictionaries in the hybrid record to JSON strings."""
    for column in COMMON_COLUMNS + ['Other']:
        if column in hybrid_record:
            hybrid_record[column] = json.dumps(hybrid_record[column])

def append_to_parquet(df, file_path):
    """Append DataFrame to a Parquet file."""
    ensure_directory_exists(file_path)
    if os.path.exists(file_path):
        existing_df = pd.read_parquet(file_path)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        table = pa.Table.from_pandas(combined_df)
        pq.write_table(table, file_path)
    else:
        table = pa.Table.from_pandas(df)
        pq.write_table(table, file_path)
        logging.info(f"Created new Parquet file: {file_path}")

def ensure_directory_exists(file_path):
    """Ensure the directory for the file path exists."""
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")

def process_items(items, base_url, items_info_path):
    """Process each item by scraping and storing data."""
    for item in items:
        url = f"{base_url}{item}"
        content = fetch_url_content(url)
        if content:
            titles_and_content = parse_html(content)
            hybrid_records = transform_records(titles_and_content, item)
            if hybrid_records:
                df_new_records = pd.DataFrame(hybrid_records)
                append_to_parquet(df_new_records, items_info_path)

def main():
    combined_file_path = 'data/combined_voting_data.parquet'
    items_info_path = 'data/items_info.parquet'
    base_url = 'https://secure.toronto.ca/council/agenda-item.do?item='

    logging.info(f"Reading agenda item IDs from {combined_file_path}")
    df_combined = pd.read_parquet(combined_file_path)
    items = df_combined['Agenda Item #'].astype(str).unique()

    if os.path.exists(items_info_path):
        logging.info(f"Reading existing items from {items_info_path}")
        df_items_info = pd.read_parquet(items_info_path)
        existing_items = df_items_info['meeting_id'].unique()
        items = [item for item in items if item not in existing_items]
    else:
        df_items_info = pd.DataFrame(columns=['meeting_id'] + COMMON_COLUMNS + ['Other'])
        df_items_info.to_parquet(items_info_path)
        logging.info(f"Created empty Parquet file: {items_info_path}")

    process_items(items, base_url, items_info_path)
    logging.info('Web scraping process completed.')

if __name__ == "__main__":
    logging.info('Starting the web scraping process.')
    main()
    logging.info('Web scraping process completed.')
