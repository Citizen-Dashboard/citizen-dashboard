import logging
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance
from sklearn.feature_extraction.text import CountVectorizer
import spacy
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class POSFilteredTfidfVectorizer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.count_vectorizer = CountVectorizer()
        self.ctfidf_transformer = ClassTfidfTransformer()

    def fit_transform(self, X):
        # First, apply POS filtering
        filtered_X = self._pos_filter(X)

        # Convert to document-term matrix
        count_matrix = self.count_vectorizer.fit_transform(filtered_X)
        
        # Apply c-TF-IDF transformation
        ctfidf_matrix = self.ctfidf_transformer.fit_transform(count_matrix)
        
        return ctfidf_matrix

    def transform(self, X):
        filtered_X = self._pos_filter(X)
        count_matrix = self.count_vectorizer.transform(filtered_X)
        return self.ctfidf_transformer.transform(count_matrix)

    def _pos_filter(self, X):
        filtered_X = []
        for doc in X:
            pos_doc = self.nlp(doc)
            filtered_doc = ' '.join([token.text for token in pos_doc if token.pos_ in ['NOUN', 'PROPN', 'ADJ']])
            filtered_X.append(filtered_doc)
        return filtered_X

    def get_feature_names_out(self):
        return self.count_vectorizer.get_feature_names_out()

def create_topic_model(umap_model, hdbscan_model, embedding_model):
    logger.info("Creating BERTopic model with improved representation")
    keybert_model = KeyBERTInspired()
    mmr_model = MaximalMarginalRelevance(diversity=0.3)
    
    vectorizer_model = POSFilteredTfidfVectorizer()
    
    topic_model = BERTopic(
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        representation_model=[keybert_model, mmr_model],
        embedding_model=embedding_model,  # Pass the embedding model here
        top_n_words=10,
        verbose=True
    )
    return topic_model

def fit_transform_topics(topic_model, texts, embeddings):
    logger.info("Fitting the BERTopic model and transforming the texts")
    topics, probs = topic_model.fit_transform(texts, embeddings)
    logger.info("Model fitting and transformation completed")
    logger.info(f"Number of topics: {len(set(topics))}")
    return topics, probs

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # For testing purposes
    from umap import UMAP
    from hdbscan import HDBSCAN
    import numpy as np

    sample_texts = ["This is a sample text", "Another example sentence", "Topic modeling is interesting"]
    sample_embeddings = np.random.rand(3, 384)  # 3 samples with 384 dimensions

    umap_model = UMAP(n_components=2, random_state=42)
    hdbscan_model = HDBSCAN(min_cluster_size=2, min_samples=1)
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device='cuda')

    topic_model = create_topic_model(umap_model, hdbscan_model, embedding_model)
    topics, probs = fit_transform_topics(topic_model, sample_texts, sample_embeddings)
    print(f"Topics: {topics}")
    print(f"Probabilities shape: {probs.shape}")