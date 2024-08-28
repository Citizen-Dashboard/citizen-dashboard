import argparse
import logging
import pandas as pd
import os
from .fetch_voting_records import fetch_voting_records
# from .processor import process_items 


logger = logging.getLogger(__name__)


def fetch_data(voting_record_url, package_id):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    combined_df = fetch_voting_records(voting_record_url, package_id)
    return combined_df
