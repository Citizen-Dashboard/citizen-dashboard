import logging
import torch
import numpy as np
from src import (
    visualize_documents, 
    create_topic_model, 
    fit_transform_topics, 
    fetch_data, 
    generate_embeddings, 
    reduce_dimensionality, 
    perform_clustering,
    preprocess_data
)
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class UmapParams:
    n_neighbors: int
    min_dist: float
    n_components: int

    def __init__(self, n_docs):
        self.n_neighbors = min(30, max(5, int(np.log2(n_docs))))
        self.min_dist = max(0.0, 0.1 - (n_docs / 10000))
        self.n_components = min(100, max(3, int(np.log2(n_docs))))


@dataclass
class HdbscanParams:
    min_cluster_size: int
    min_samples: int

    def __init__(self, n_docs):
        self.min_cluster_size = max(5, int(np.log2(n_docs)))
        self.min_samples = max(5, self.min_cluster_size // 2)

@dataclass
class BertopicParams:
    top_n_words: int
    def __init__(self, n_docs):
        self.top_n_words = min(20, max(5, int(np.log2(n_docs))))


@dataclass
class PipelineParams:
    n_docs: int
    umap_params: UmapParams
    hdbscan_params: HdbscanParams
    bertopic_params: BertopicParams

    def __init__(self, n_docs):
        self.umap_params = UmapParams(n_docs)
        self.hdbscan_params = HdbscanParams(n_docs)
        self.bertopic_params = BertopicParams(n_docs)        


def process_committee_data(committee, committee_data, embedding_model):
    logger.info(f"Processing data for committee: {committee}")
    
    # Preprocess data for this council member
    voting_data, texts = preprocess_data(committee_data)
    n_docs = len(texts) 
    pipeline_params = PipelineParams(n_docs)
    # Generate embeddings
    embeddings = generate_embeddings(texts, embedding_model)
    
    # Reduce dimensionality
    reduced_embeddings, umap_model = reduce_dimensionality(
        embeddings, 
        n_neighbors=pipeline_params.umap_params.n_neighbors,
        n_components=pipeline_params.umap_params.n_components,
        min_dist=pipeline_params.umap_params.min_dist
        )
    
    # Perform clustering
    clusters, hdbscan_model = perform_clustering(
        reduced_embeddings, 
        min_cluster_size=pipeline_params.hdbscan_params.min_cluster_size, 
        min_samples=pipeline_params.hdbscan_params.min_samples
        )
    
    # Create and fit topic model
    topic_model = create_topic_model(
        umap_model, 
        hdbscan_model, 
        embedding_model, 
        top_n_words=pipeline_params.bertopic_params.top_n_words
        )
    topics, probs = fit_transform_topics(topic_model, texts, embeddings)
    
    # Visualize results
    fig = visualize_documents(topic_model=topic_model, docs=texts, voting_data=voting_data, topics=topics, embeddings=embeddings, reduced_embeddings=reduced_embeddings)
    fig.write_html(f"3d_topics_visualization_{committee}.html")
    logger.info(f"3D visualization for {committee} saved as 3d_topics_visualization_{committee}.html")

def main():
    # Fetch data
    base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    package_id = "members-of-toronto-city-council-voting-record"
    combined_df = fetch_data(base_url, package_id, from_local=True, local_file_path="./data/combined_data.parquet")
    
    # Create full name column
    combined_df['Full Name'] = combined_df['First Name'] + ' ' + combined_df['Last Name']
    
    # Initialize the embedding model
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device='cuda' if torch.cuda.is_available() else 'cpu')
    
    # Group by committee and process each group
    for council_name, council_data in combined_df.groupby('Committee'):
        if len(council_data.index) > 1000 and len(council_data['Agenda Item Title'].unique()) > 100:
            process_committee_data(council_name, council_data, embedding_model)

if __name__ == "__main__":
    main()
