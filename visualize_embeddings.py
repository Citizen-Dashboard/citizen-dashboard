import logging
import requests
import pandas as pd
import io
import warnings
from bertopic import BERTopic
from cuml.cluster import HDBSCAN
from sentence_transformers import SentenceTransformer
from cuml.manifold import UMAP
import torch
import numpy as np
import plotly.graph_objects as go

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Check CUDA availability
cuda_available = torch.cuda.is_available()
logger.info(f"CUDA Available: {cuda_available}")

# Define the base URL and package ID
base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
package_id = "members-of-toronto-city-council-voting-record"

# Fetch package metadata
logger.info("Fetching package metadata...")
package_url = f"{base_url}/api/3/action/package_show"
params = {"id": package_id}
package_response = requests.get(package_url, params=params)
package_data = package_response.json()

# Check if the request was successful
if not package_data['success']:
    logger.error("Failed to fetch package metadata")
    raise Exception("Failed to fetch package metadata")
logger.info("Package metadata fetched successfully")

# Initialize an empty list to store DataFrames
dataframes = []

# Loop through resources and fetch data
for resource in package_data["result"]["resources"]:
    if resource["datastore_active"]:
        logger.info(f"Fetching data for resource: {resource['name']}")
        # Fetch data in CSV format
        csv_url = f"{base_url}/datastore/dump/{resource['id']}"
        csv_data = requests.get(csv_url).text
        
        # Convert CSV data to DataFrame
        try:
            df = pd.read_csv(io.StringIO(csv_data))
            dataframes.append(df)
            logger.info(f"Data fetched and converted to DataFrame for resource: {resource['name']}")
        except pd.errors.ParserError as e:
            logger.warning(f"Error parsing {resource['name']}: {e}")
        except Exception as e:
            logger.warning(f"An error occurred while processing {resource['name']}: {e}")

# Combine all DataFrames into one (if there are multiple)
if dataframes:
    combined_df = pd.concat(dataframes, ignore_index=True)
    logger.info("Combined all DataFrames into one")
    logger.info(f"Combined DataFrame head:\n{combined_df.head()}")
else:
    logger.warning("No datastore active resources found")

# Save the combined DataFrame to a CSV file (optional)
# combined_df.to_csv("combined_data.csv", index=False)

# Extract text data from the "Agenda Item Title" column
texts = combined_df['Agenda Item Title'].unique()
logger.info(f"Extracted {len(texts)} unique texts from the 'Agenda Item Title' column")

# Load a pre-trained sentence transformer model with GPU support
logger.info("Loading pre-trained sentence transformer model with GPU support")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device='cuda')

# Generate embeddings using the GPU
logger.info("Generating embeddings using the GPU")
embeddings = embedding_model.encode(texts, show_progress_bar=True)
logger.info(f"Embeddings generated with shape: {embeddings.shape}")

# Save the embeddings to a .npy file
# np.save("embeddings.npy", embeddings)
# logger.info("Embeddings saved to embeddings.npy")

# Load the embeddings from the .npy file (if needed)
# embeddings = np.load("embeddings.npy")
# logger.info("Embeddings loaded from embeddings.npy")

# Use GPU-accelerated UMAP to reduce dimensionality to 3D
logger.info("Using GPU-accelerated UMAP to reduce dimensionality to 3D")
umap_model = UMAP(n_components=3, n_neighbors=100, min_dist=0.01, metric='cosine')
reduced_embeddings = umap_model.fit_transform(embeddings)
logger.info(f"Dimensionality reduction completed with shape: {reduced_embeddings.shape}")

# Use GPU-accelerated HDBSCAN for clustering
logger.info("Using GPU-accelerated HDBSCAN for clustering")
hdbscan_model = HDBSCAN(min_cluster_size=60, min_samples=30, cluster_selection_method='leaf', gen_min_span_tree=True, prediction_data=True)
clusters = hdbscan_model.fit_predict(reduced_embeddings)
logger.info(f"Clustering completed with {len(set(clusters))} clusters")

# Create a BERTopic model with GPU-accelerated UMAP and HDBSCAN
logger.info("Creating BERTopic model with GPU-accelerated UMAP and HDBSCAN")
topic_model = BERTopic(umap_model=umap_model, hdbscan_model=hdbscan_model, top_n_words=20, n_gram_range=(1, 2), low_memory=True, verbose=True)

# Fit the model and transform the texts
logger.info("Fitting the BERTopic model and transforming the texts")
topics, probs = topic_model.fit_transform(texts, embeddings)
logger.info("Model fitting and transformation completed")
logger.info(f"Number of topics: {len(set(topics))}")

# Create hierarchical topics
logger.info("Creating hierarchical topics")
hierarchical_topics = topic_model.hierarchical_topics(texts)
logger.info("Hierarchical topics created")

# Function to visualize documents in 3D
def visualize_documents(topic_model, docs, topics=None, embeddings=None, reduced_embeddings=None, sample=None,
                        hide_annotations=False, hide_document_hover=False, custom_labels=False, width=1200, height=750):
    """ Visualize documents and their topics in 3D """
    topic_per_doc = topic_model.topics_

    # Sample the data to optimize for visualization and dimensionality reduction
    if sample is None or sample > 1:
        sample = 1
    indices = []
    for topic in set(topic_per_doc):
        s = np.where(np.array(topic_per_doc) == topic)[0]
        size = len(s) if len(s) < 100 else int(len(s) * sample)
        indices.extend(np.random.choice(s, size=size, replace=False))
    indices = np.array(indices)

    df = pd.DataFrame({"topic": np.array(topic_per_doc)[indices]})
    df["doc"] = [docs[index] for index in indices]
    df["topic"] = [topic_per_doc[index] for index in indices]

    # Extract embeddings if not already done
    if sample is None:
        if embeddings is None and reduced_embeddings is None:
            embeddings_to_reduce = topic_model._extract_embeddings(df.doc.to_list(), method="document")
        else:
            embeddings_to_reduce = embeddings
    else:
        if embeddings is not None:
            embeddings_to_reduce = embeddings[indices]
        elif embeddings is None and reduced_embeddings is None:
            embeddings_to_reduce = topic_model._extract_embeddings(df.doc.to_list(), method="document")

    # Reduce input embeddings
    if reduced_embeddings is None:
        umap_model = UMAP(n_neighbors=10, n_components=3, min_dist=0.0, metric='cosine').fit(embeddings_to_reduce)
        embeddings_2d = umap_model.embedding_
    elif sample is not None and reduced_embeddings is not None:
        embeddings_2d = reduced_embeddings[indices]
    elif sample is None and reduced_embeddings is not None:
        embeddings_2d = reduced_embeddings

    unique_topics = set(topic_per_doc)
    if topics is None:
        topics = unique_topics

    # Combine data
    df["x"] = embeddings_2d[:, 0]
    df["y"] = embeddings_2d[:, 1]
    df["z"] = embeddings_2d[:, 2]

    # Prepare text and names
    if topic_model.custom_labels_ is not None and custom_labels:
        names = [topic_model.custom_labels_[topic + topic_model._outliers] for topic in unique_topics]
    else:
        names = [f"{topic}_" + "_".join([word for word, value in topic_model.get_topic(topic)][:3]) for topic in unique_topics]

    # Visualize
    fig = go.Figure()

    # Outliers and non-selected topics
    non_selected_topics = set(unique_topics).difference(topics)
    if len(non_selected_topics) == 0:
        non_selected_topics = [-1]
    selection = df.loc[df.topic.isin(non_selected_topics), :]
    selection["text"] = ""
    selection.loc[len(selection), :] = [None, None, selection.x.mean(), selection.y.mean(), selection.z.mean(), "Other documents"]
    fig.add_trace(
        go.Scatter3d(
            x=selection.x,
            y=selection.y,
            z=selection.z,
            hovertext=selection.doc if not hide_document_hover else None,
            hoverinfo="text",
            mode='markers+text',
            name="other",
            showlegend=False,
            marker=dict(color='#CFD8DC', size=5, opacity=0.5)
        )
    )

    # Selected topics
    for name, topic in zip(names, unique_topics):
        if topic in topics and topic != -1:
            selection = df.loc[df.topic == topic, :]
            selection["text"] = ""
            if not hide_annotations:
                selection.loc[len(selection), :] = [None, None, selection.x.mean(), selection.y.mean(), selection.z.mean(), name]
            fig.add_trace(
                go.Scatter3d(
                    x=selection.x,
                    y=selection.y,
                    z=selection.z,
                    hovertext=selection.doc if not hide_document_hover else None,
                    hoverinfo="text",
                    text=selection.text,
                    mode='markers+text',
                    name=name,
                    textfont=dict(size=12),
                    marker=dict(size=5, opacity=0.5)
                )
            )

    # Add grid in a 'plus' shape
    x_range = (df.x.min() - abs((df.x.min()) * .15), df.x.max() + abs((df.x.max()) * .15))
    y_range = (df.y.min() - abs((df.y.min()) * .15), df.y.max() + abs((df.y.max()) * .15))
    fig.add_shape(type="line",
                  x0=sum(x_range) / 2, y0=y_range[0], x1=sum(x_range) / 2, y1=y_range[1],
                  line=dict(color="#CFD8DC", width=2))
    fig.add_shape(type="line",
                  x0=x_range[0], y0=sum(y_range) / 2, x1=x_range[1], y1=sum(y_range) / 2,
                  line=dict(color="#9E9E9E", width=2))
    fig.add_annotation(x=x_range[0], y=sum(y_range) / 2, text="D1", showarrow=False, yshift=10)
    fig.add_annotation(y=y_range[1], x=sum(x_range) / 2, text="D2", showarrow=False, xshift=10)

    # Stylize layout
    fig.update_layout(
        template="simple_white",
        title={
            'text': "Documents and Topics",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=22, color="Black")
        },
        width=width,
        height=height
    )

    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)

    return fig

# Visualize the hierarchical documents in 3D
logger.info("Visualizing the hierarchical documents in 3D")
fig = visualize_documents(topic_model, texts, topics=topics, embeddings=embeddings, reduced_embeddings=reduced_embeddings)

# Save the visualization as an interactive HTML file
fig.write_html("3d_topics_visualization.html")
logger.info("3D visualization saved as 3d_topics_visualization.html")

# Optionally, show the plot (if running in an environment that supports it)
# fig.show()