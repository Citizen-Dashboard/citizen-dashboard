from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from typing import List

from app_logging.logger import File_Console_Logger

logger = File_Console_Logger(__name__)

load_dotenv()
promptTemplate = """With the following piece of topic, generate a summary of the content less than 100 words. You must be impartial, non-judgemental and gender neutral. Use only the information provided in the context.
Your response should strictly be in JSON format shown in the example.
{example}
---
{topic}
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
        self.rag_chain = self.prompt | gpt_3_5_llm | self.json_parser
        self.example = "{\"summary\": \"This is a concise summary of the provided context that is impartial, non-judgmental and gender neutral.\"}"
    
    def summarizeTextContent(self, TextContent):
        response = self.rag_chain.invoke({"topic":TextContent, "example":self.example})
        logger.debug(response)
        return response


    