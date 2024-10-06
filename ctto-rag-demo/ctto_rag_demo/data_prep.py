from langchain_openai import ChatOpenAI
from .vectordb.milvus_vector_store import vectorstore
from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .scraper import tmmis_agenda_items_scraper
import os
from dotenv import load_dotenv
from .rag import initRagChain,query
from .server import startApp

load_dotenv()

gpt_4_mini_llm = ChatOpenAI(model="gpt-4o-mini")
gpt_3_5_llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=50, add_start_index=True
    )

embeddings = OpenAIEmbeddings()
# vectorstore = None
retriever = None
# https://secure.toronto.ca/council/agenda-item.do?item=2024.EC14.1
# https://secure.toronto.ca/council/report.do?meeting=2024.EC14&type=agenda

def parse_data():
    # Get each agenda item as a list for meeting number 2024.IE14
    textList, docList = tmmis_agenda_items_scraper("2024.IE14").getAgendaItems()
    # print(docList)

    # Next, we'll use RecursiveCharacterSplitter to split our data into digestable chunks for our LLM
    # We'll convert them to vector with openAIEmbeddings and save in vector DB
    # for docItem in docList:
    chunk = split_agenda_item(docList)
    storeOpenAiEmbeddings(chunk)

def storeOpenAiEmbeddings(textChunk):
    vectorstore.add_documents(textChunk)

# def storeOpenAiEmbeddings(textChunk):
#     global vectorStore
#     if(vectorStore is None):
#         vectorStore = Chroma.from_documents(documents=textChunk, embedding=OpenAIEmbeddings())
#     else:
#         Chroma.add_documents(textChunk)


def split_agenda_item(agendaItem):
    return text_splitter.split_documents(agendaItem)



def startRAG():
    setupRetriever()
    # testRetrieval()

    #initialize RAG
    initRagChain(retriever, gpt_3_5_llm)
    
    #start fast api server
    startApp()
    
def setupRetriever():
    # global vectorStore
    global retriever
    if(vectorstore is None):
        print("Vector Store undefined")
        return
    
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

def testRetrieval():
    retrieved_docs = retriever.invoke("What are the approaches to Cycling?")



if __name__ == "__main__":
    # Use parse_data to add new documents to vector store
    # or to initilize vector store.
    # keep commented if vector store is already setup.
    parse_data()
    startRAG()
    