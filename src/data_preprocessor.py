import logging
import pandas as pd

logger = logging.getLogger(__name__)

def preprocess_data(dataframes):
    logger.info("Preprocessing data...")
    if not dataframes:
        logger.warning("No dataframes to process")
        return None, []

    combined_df = pd.concat(dataframes, ignore_index=True)
    logger.info("Combined all DataFrames into one")
    logger.info(f"Combined DataFrame shape: {combined_df.shape}")

    texts = combined_df['Agenda Item Title'].unique()
    logger.info(f"Extracted {len(texts)} unique texts from the 'Agenda Item Title' column")

    return combined_df, texts

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # For testing purposes, create some sample dataframes
    df1 = pd.DataFrame({'Agenda Item Title': ['Item 1', 'Item 2', 'Item 3']})
    df2 = pd.DataFrame({'Agenda Item Title': ['Item 3', 'Item 4', 'Item 5']})
    dataframes = [df1, df2]

    combined_df, texts = preprocess_data(dataframes)
    print(f"Combined DataFrame:\n{combined_df}")
    print(f"Unique texts: {texts}")