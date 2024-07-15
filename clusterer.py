import logging
from cuml.cluster import HDBSCAN

logger = logging.getLogger(__name__)

def perform_clustering(reduced_embeddings, min_cluster_size=60, min_samples=30):
    logger.info("Performing clustering using HDBSCAN")
    hdbscan_model = HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, 
                            cluster_selection_method='leaf', gen_min_span_tree=True, prediction_data=True)
    clusters = hdbscan_model.fit_predict(reduced_embeddings)
    logger.info(f"Clustering completed with {len(set(clusters))} clusters")
    return clusters, hdbscan_model

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # For testing purposes
    import numpy as np
    sample_reduced_embeddings = np.random.rand(100, 3)  # 100 samples with 3 dimensions
    clusters, _ = perform_clustering(sample_reduced_embeddings)
    print(f"Number of clusters: {len(set(clusters))}")