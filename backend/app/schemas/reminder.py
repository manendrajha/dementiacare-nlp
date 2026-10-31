
from pydantic import BaseModel, Field, ConfigDict


class ReminderCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    time: str = Field(pattern=r"^([01]\d|2[0-3]):[0-5]\d$")


class ReminderUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    time: str = Field(pattern=r"^([01]\d|2[0-3]):[0-5]\d$")


class ReminderResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    title: str
    description: str
    time: str
