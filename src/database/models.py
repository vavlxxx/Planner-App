from typing import List, Optional

from pydantic import EmailStr
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    image: str 
    description: str
    tags: List[str] = Field(sa_column=Column(JSON))
    location: str
    user_id: int = Field(foreign_key="user.id")
    creator: Optional["User"] = Relationship(back_populates="events")

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet",
                "user_id": 1
            }
        }


class EventUpdate(SQLModel): 
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None
    user_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "location": "Google Meet"
            }
        }


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    password: str
    events: List["Event"] = Relationship(back_populates="creator")
    
    class Config:
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
                "events": []
            }
        }


class UserSignIn(SQLModel):
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra={
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!"
            }
        }


class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    events: Optional[List[int]] = None
    
    class Config:
        json_schema_extra={
            "example": {
                "email": "newemail@packt.com",
                "password": "newpassword!!!"
            }
        }

class EventRead(SQLModel):
    id: int
    title: str
    image: str
    description: str
    tags: List[str]
    location: str
    user_id: Optional[int] = None


class UserRead(SQLModel):
    id: int
    email: EmailStr
    events: List[EventRead] = []