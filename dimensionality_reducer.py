import logging
from cuml.manifold import UMAP

logger = logging.getLogger(__name__)

def reduce_dimensionality(embeddings, n_components=3, n_neighbors=100, min_dist=0.01, metric='cosine'):
    logger.info(f"Reducing dimensionality to {n_components}D using UMAP")
    umap_model = UMAP(n_components=n_components, n_neighbors=n_neighbors, min_dist=min_dist, metric=metric)
    reduced_embeddings = umap_model.fit_transform(embeddings)
    logger.info(f"Dimensionality reduction completed with shape: {reduced_embeddings.shape}")
    return reduced_embeddings, umap_model

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # For testing purposes
    import numpy as np
    sample_embeddings = np.random.rand(100, 384)  # 100 samples with 384 dimensions
    reduced_embeddings, _ = reduce_dimensionality(sample_embeddings)
    print(f"Reduced embeddings shape: {reduced_embeddings.shape}")