from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage , SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def printResponse(text):
    print(text)
    return text

rag_chain = None



def initRagChain(retriever, llm):
    global rag_chain

    promptTemplate =  """Use the following pieces of context to answer the question at the end. If the necessary information is not available within the context provided, or if you don't know the answer, just say that you don't know, don't try to make up an answer.
Keep the answer as concise as possible. But you may respond with up to ten sentences if the human asks to give details.
Occasionally say "thanks for asking!" at the end of the answer.

{context}

Question: {question}

Helpful Answer:"""
    

    prompt = PromptTemplate.from_template(promptTemplate)


    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )


def getChain():
    return rag_chain

def query(queryString):
    global rag_chain
    return rag_chain.invoke(queryString)