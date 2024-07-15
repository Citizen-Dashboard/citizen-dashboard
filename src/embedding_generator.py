import logging
from sentence_transformers import SentenceTransformer
import torch

logger = logging.getLogger(__name__)

def generate_embeddings(texts, model_name="all-MiniLM-L6-v2"):
    logger.info("Loading pre-trained sentence transformer model")
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    embedding_model = SentenceTransformer(model_name, device=device)

    logger.info(f"Generating embeddings using {device.upper()}")
    embeddings = embedding_model.encode(texts, show_progress_bar=True)
    logger.info(f"Embeddings generated with shape: {embeddings.shape}")

    return embeddings

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # For testing purposes
    sample_texts = ["This is a sample text", "Another example sentence", "Topic modeling is interesting"]
    embeddings = generate_embeddings(sample_texts)
    print(f"Sample embedding shape: {embeddings.shape}")