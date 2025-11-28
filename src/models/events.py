from typing import List, Optional
from pydantic import BaseModel, ConfigDict, model_validator
from beanie import Document


class EventBase(BaseModel):
    title: str
    image: str
    description: str
    user_id: str
    tags: List[str]
    location: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with you own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet",
            },
        }
    )


class EventMongo(EventBase, Document): ...


class Event(EventBase):
    id: str

    @model_validator(mode="before")
    @classmethod
    def serialize(cls, data) -> dict:
        data["id"] = str(data["id"])
        return data


class EventUpdate(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    user_id: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https: //linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet",
            }
        }
