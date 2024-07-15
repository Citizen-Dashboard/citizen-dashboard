import logging
from src import (
    visualize_documents, 
    create_topic_model, 
    fit_transform_topics, 
    fetch_data, 
    preprocess_data, 
    generate_embeddings, 
    reduce_dimensionality, 
    perform_clustering
    )
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Fetch data
    base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    package_id = "members-of-toronto-city-council-voting-record"
    dataframes = fetch_data(base_url, package_id)

    # Preprocess data
    combined_df, texts = preprocess_data(dataframes)

    # Generate embeddings
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device='cuda')
    embeddings = generate_embeddings(texts)

    # Reduce dimensionality
    reduced_embeddings, umap_model = reduce_dimensionality(embeddings)

    # Perform clustering
    clusters, hdbscan_model = perform_clustering(reduced_embeddings)

    # Create and fit topic model
    topic_model = create_topic_model(umap_model, hdbscan_model, embedding_model)
    topics, probs = fit_transform_topics(topic_model, texts, embeddings)

    # Visualize results
    fig = visualize_documents(topic_model, texts, topics=topics, embeddings=embeddings, reduced_embeddings=reduced_embeddings)
    fig.write_html("3d_topics_visualization.html")
    logger.info("3D visualization saved as 3d_topics_visualization.html")

if __name__ == "__main__":
    main()