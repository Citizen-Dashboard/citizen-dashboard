from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from pydantic import BaseModel, Field
import os
import json
from dotenv import load_dotenv
load_dotenv()
print("*** ",os.environ.get("log_level"))

from typing import List

# from app_logging.logger import File_Console_Logger

# logger = File_Console_Logger(__name__)

promptTemplate = """You will be given a topic and set of recommendations and decisions from a meeting. Generate a synopsis of the meeting and the recommendations or decisions made in less than 150 words. You must be impartial, non-judgemental and gender neutral. Use only the information provided in the context.
Your response should strictly be in JSON format shown in the example.
{example}
---
{topic}

{recommendations}

{decision}
""" 
# gpt_4_mini_llm = ChatOpenAI(model="gpt-4o-mini")
gpt_3_5_llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=50, add_start_index=True
    )

embeddings = OpenAIEmbeddings()
retriever = None


class Summary(BaseModel):
    summary: str = Field(description="summary of a context")

class Summaizer:
    def __init__(self):
        """Initialize the Summarizer class.
        
        Sets up the JSON output parser and example format for the prompt template.
        """
        self.json_parser = JsonOutputParser(pydantic_object=Summary)
        self.str_parser = StrOutputParser()
        self.prompt = PromptTemplate.from_template(promptTemplate)
        self.rag_chain = self.prompt | gpt_3_5_llm
        self.example = \
        """{"summary":"this is a concise summary of the provided topic including recommendations and decisions"}"""
    
    def summarizeTextContent(self, topic, recommendations, decision):
        response = self.rag_chain.invoke({"topic":topic, "recommendations":recommendations, "decision":decision, "example":self.example})
        try:
            response = self.json_parser.invoke(response)
        except Exception as e:
            response =self.str_parser.invoke(response)

        # logger.debug(response)
        return response


    