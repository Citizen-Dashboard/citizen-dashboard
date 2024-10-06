from langchain_milvus.vectorstores import Milvus
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
import os

milvus_connection_string = os.environ["MILVUS_CONNECTION_STRING"]
embeddings = OpenAIEmbeddings()

vectorstore = Milvus(embeddings, connection_args={"uri": milvus_connection_string}, collection_name="agenda_items_collection_v1")
vectorstore.auto_id = True


