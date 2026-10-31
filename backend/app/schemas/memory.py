
from pydantic import BaseModel, Field, ConfigDict


class MemoryCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    category: str = Field(default="People", max_length=50)


class MemoryUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    category: str = Field(default="People", max_length=50)


class MemoryResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    title: str
    description: str
    category: str
