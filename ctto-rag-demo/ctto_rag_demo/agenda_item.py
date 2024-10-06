from pydantic import BaseModel, Field
class AgendaItem(BaseModel):
    summary:str = Field(description="Summary of the agenda item")