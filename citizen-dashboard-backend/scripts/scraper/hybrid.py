import logging
import os
import pandas as pd
import random
import requests
import time
import json
from bs4 import BeautifulSoup

def process_items(items, base_url, items_info_path, min_wait, max_wait, table_layout):
    for item in items:
        url = f"{base_url}{item}"
        content = fetch_url_content(url)
        if content:
            titles_and_content = parse_html(content)
            hybrid_records = transform_records(titles_and_content, item, table_layout)
            if hybrid_records:
                df_new_records = pd.DataFrame(hybrid_records)
                append_to_csv(df_new_records, items_info_path)
        time.sleep(get_random_wait(min_wait, max_wait))

def get_random_wait(min_wait, max_wait):
    """Generate a random wait time between given min and max wait values."""
    wait_time = random.uniform(min_wait, max_wait)
    logging.info(f'Waiting for {wait_time:.2f} seconds before making the next request.')
    return wait_time

def fetch_url_content(url):
    """Fetch the content of a URL."""
    logging.info(f'Starting to scrape URL: {url}')
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info(f'Successfully fetched content from URL: {url}')
        return response.content
    except requests.RequestException as e:
        logging.error(f'Failed to fetch content from URL: {url}, Error: {e}')
        return None

def parse_html(content):
    """Parse HTML content to extract titles and content."""
    soup = BeautifulSoup(content, 'html.parser')
    return [extract_title_and_content(h4) for h4 in soup.find_all('h4') if "Confidential" not in h4.get_text(strip=True)]

def extract_title_and_content(h4):
    """Extract title and content from an h4 tag."""
    title = h4.get_text(strip=True)
    content = extract_content(h4)
    return {"title": title, "content": content}

def extract_content(h4_tag):
    """Extract content following an h4 tag."""
    content = []
    for sibling in h4_tag.find_next_siblings():
        if sibling.name == 'h4':
            break
        content.append(sibling.get_text(strip=True))
    return ' '.join(content)

def categorize_title(title, table_layout):
    """Categorize a title based on the appears_as or name fields."""
    for column in table_layout:
        appears_as = column.get('appears_as', '').lower()
        name = column['name'].lower()
        if appears_as and appears_as in title.lower():
            return column['name'], title.replace(appears_as, '').strip()
        elif name in title.lower():
            return column['name'], 'default'
    return 'other', title

def transform_records(records, item_id, table_layout):
    """Transform records into a hybrid format."""
    hybrid_record = {"item_id": item_id}
    for record in records:
        title, key = categorize_title(record['title'], table_layout)
        add_content_to_record(hybrid_record, title, key, record['content'])
    convert_dicts_to_json(hybrid_record, table_layout)
    return [hybrid_record]

def add_content_to_record(hybrid_record, title, key, content):
    """Add content to the hybrid record."""
    if title not in hybrid_record:
        hybrid_record[title] = {}
    if key in hybrid_record[title]:
        hybrid_record[title][key] += ' ' + content
    else:
        hybrid_record[title][key] = content

def convert_dicts_to_json(hybrid_record, table_layout):
    """Convert dictionaries in the hybrid record to JSON strings."""
    for column in [column['name'] for column in table_layout] + ['other']:
        if column in hybrid_record:
            hybrid_record[column] = json.dumps(hybrid_record[column], ensure_ascii=False)

def append_to_csv(df, file_path):
    """Append DataFrame to a CSV file."""
    ensure_directory_exists(file_path)
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_csv(file_path, index=False, quoting=pd.io.common.CSV_QUOTE_NONE, escapechar=' ')
    else:
        df.to_csv(file_path, index=False, quoting=pd.io.common.CSV_QUOTE_NONE, escapechar=' ')
        logging.info(f"Created new CSV file: {file_path}")

def ensure_directory_exists(file_path):
    """Ensure the directory for the file path exists."""
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")
