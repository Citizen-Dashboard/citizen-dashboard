import requests
from bs4 import BeautifulSoup
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import random
import time
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_random_wait():
    wait_time = random.uniform(1, 5)  # Random wait time between 1 and 5 seconds
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
        return {}
    soup = BeautifulSoup(response.content, 'html.parser')
    titles_and_content = {}
    for h4 in soup.find_all('h4'):
        title = h4.get_text(strip=True)
        if "Confidential" in title:
            continue  # Skip titles containing "Confidential"
        content = []
        for sibling in h4.find_next_siblings():
            if sibling.name == 'h4':
                break
            content.append(sibling.get_text(strip=True))
        titles_and_content[title] = ' '.join(content)
    logging.info(f'Extracted {len(titles_and_content)} titles and content from URL: {url}')
    return titles_and_content

def align_schemas(existing_df, new_df):
    # Ensure both DataFrames have the same columns
    for column in existing_df.columns:
        if column not in new_df.columns:
            new_df[column] = None
    for column in new_df.columns:
        if column not in existing_df.columns:
            existing_df[column] = None
    return existing_df, new_df

def append_to_parquet(df, file_path):
    if os.path.exists(file_path):
        existing_df = pd.read_parquet(file_path)
        existing_df, df = align_schemas(existing_df, df)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        table = pa.Table.from_pandas(combined_df)
        pq.write_table(table, file_path)
    else:
        table = pa.Table.from_pandas(df)
        pq.write_table(table, file_path)

def main():
    # Read the Parquet file to get the agenda item IDs
    logging.info('Reading agenda item IDs from combined_data.parquet')
    df_combined = pd.read_parquet('data/combined_data.parquet')
    items = df_combined['Agenda Item #'].astype(str).unique()  # Ensure agenda item IDs are strings
    base_url = 'https://secure.toronto.ca/council/agenda-item.do?item='
    urls = [base_url + item for item in items]

    file_path_non_vote = 'data/items_info.parquet'
    file_path_vote = 'data/items_votes.parquet'
    max_pages = 10
    page_count = 0

    for item, url in zip(items, urls):
        if page_count >= max_pages:
            logging.info(f'Termination variable reached: {max_pages} pages scraped.')
            break
        if os.path.exists(file_path_non_vote):
            existing_df_non_vote = pd.read_parquet(file_path_non_vote)
            if item in existing_df_non_vote['Agenda Item #'].values:
                logging.info(f'Agenda item {item} already recorded in non-vote file. Skipping...')
                continue
        if os.path.exists(file_path_vote):
            existing_df_vote = pd.read_parquet(file_path_vote)
            if item in existing_df_vote['Agenda Item #'].values:
                logging.info(f'Agenda item {item} already recorded in vote file. Skipping...')
                continue

        titles_and_content = extract_h4_titles_and_content(url)
        titles_and_content['Agenda Item #'] = item  # Add agenda item ID to the data

        # Separate data based on whether the title starts with "Vote"
        vote_data = {k: v for k, v in titles_and_content.items() if k.startswith('Vote')}
        non_vote_data = {k: v for k, v in titles_and_content.items() if not k.startswith('Vote')}

        if vote_data:
            logging.info('Appending new vote data to Parquet file.')
            vote_rows = [{'Agenda Item #': item, 'Vote Content': content} for title, content in vote_data.items()]
            vote_df = pd.DataFrame(vote_rows)
            append_to_parquet(vote_df, file_path_vote)

        if non_vote_data:
            non_vote_data['Agenda Item #'] = item
            logging.info('Appending new non-vote data to Parquet file.')
            non_vote_df = pd.DataFrame([non_vote_data])
            append_to_parquet(non_vote_df, file_path_non_vote)

        page_count += 1

    logging.info('Web scraping process completed.')

if __name__ == "__main__":
    logging.info('Starting the web scraping process.')
    main()
    logging.info('Web scraping process completed.')
