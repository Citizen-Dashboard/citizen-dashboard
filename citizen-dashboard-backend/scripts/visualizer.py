import math
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from umap import UMAP
import logging 

logger = logging.getLogger(__name__)

def preprocess_data(dataframes):
    logger.info("Preprocessing data...")
    if not dataframes:
        logger.warning("No dataframes to process")
        return None, []

    combined_df = pd.concat(dataframes, ignore_index=True)
    logger.info("Combined all DataFrames into one")
    logger.info(f"Combined DataFrame shape: {combined_df.shape}")

    # Extract unique agenda items and their corresponding voting data
    unique_agenda_items = combined_df.groupby('Agenda Item Title').first().reset_index()
    
    texts = unique_agenda_items['Agenda Item Title'].tolist()
    
    # Extract voting data and results
    voting_data = unique_agenda_items[['Agenda Item Title', 'Vote', 'Result']]
    
    # Get the list of council members
    council_members = combined_df['First Name'].unique().tolist()
    
    # Add voting data for each council member
    for member in council_members:
        voting_data[member] = combined_df[combined_df['First Name'] == member].groupby('Agenda Item Title')['Vote'].first()

    logger.info(f"Extracted {len(texts)} unique texts from the 'Agenda Item Title' column")
    return voting_data, texts

def  visualize_documents(topic_model, docs, voting_data, topics=None, embeddings=None, reduced_embeddings=None, sample=None,
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

    # Prepare hover text
    hover_texts = []
    for doc in df["doc"]:
        vote_info = voting_data[voting_data['Agenda Item Title'] == doc].iloc[0]
        hover_text = f"<b>{doc}</b><br>"
        hover_text += f"Date/Time: {vote_info['Date/Time']}<br>"
        hover_text += f"Result: {vote_info['Result']}<br>"
        hover_text += f"Overall Vote: {vote_info['Vote']}<br><br>"
        hover_text += "Council Member Votes:<br>"
        for column in vote_info.index:
            if "Vote_" in column:
                if not pd.isnull(vote_info[column]):
                    hover_text += f"{column}: {vote_info[column]}<br>"
        
        # Create a hyperlink for the "Read More" text
        read_more_link = f"<a href='https://secure.toronto.ca/council/agenda-item.do?item={vote_info['Agenda Item #']}' target='_blank'>Read More</a>"
        hover_text += f"{read_more_link}<br>"
        
        hover_texts.append(hover_text)

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
            hovertext=[hover_texts[i] for i in selection.index] if not hide_document_hover else None,
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
                    hovertext=[hover_texts[i] for i in selection.index] if not hide_document_hover else None,
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

