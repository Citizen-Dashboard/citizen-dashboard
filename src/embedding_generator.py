import logging
from sentence_transformers import SentenceTransformer
import torch

logger = logging.getLogger(__name__)

def generate_embeddings(texts, model: SentenceTransformer):
    logger.info("Loading pre-trained sentence transformer model")
    embedding_model = model

    logger.info(f"Generating embeddings")
    embeddings = embedding_model.encode(texts, show_progress_bar=True)
    logger.info(f"Embeddings generated with shape: {embeddings.shape}")

    return embeddings

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # For testing purposes
    sample_texts = ["This is a sample text", "Another example sentence", "Topic modeling is interesting"]
    embeddings = generate_embeddings(sample_texts)
    print(f"Sample embedding shape: {embeddings.shape}")