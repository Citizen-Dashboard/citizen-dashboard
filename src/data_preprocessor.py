import logging
import pandas as pd

logger = logging.getLogger(__name__)

def preprocess_data(combined_df):
    logger.info("Preprocessing data...")

    # Combine First Name and Last Name
    combined_df['Full Name'] = combined_df['First Name'] + ' ' + combined_df['Last Name']

    # Extract unique agenda items and their corresponding voting data
    voting_data = combined_df.groupby('Agenda Item Title').first().reset_index()
    
    texts = voting_data['Agenda Item Title'].tolist()
    
    
    # Get the list of council members
    council_members = combined_df['Full Name'].unique().tolist()
    
    # Add voting data for each council member
    for member in council_members:
        member_votes = combined_df[combined_df['Full Name'] == member].groupby('Agenda Item Title')['Vote'].first()
        voting_data = voting_data.join(member_votes, on='Agenda Item Title', rsuffix=f'_{member}')

    logger.info(f"Extracted {len(texts)} unique texts from the 'Agenda Item Title' column")
    return voting_data, texts
