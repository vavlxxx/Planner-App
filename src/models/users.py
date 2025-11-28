from pydantic import BaseModel, EmailStr, ConfigDict, model_validator
from typing import Optional, List
from beanie import Document
from src.models.events import Event


class UserBase(BaseModel):
    email: EmailStr
    password: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
                "events": [],
            }
        }
    )


class User(UserBase):
    id: str
    events: Optional[List[Event]] = []

    @model_validator(mode="before")
    @classmethod
    def serialize(cls, data) -> dict:
        data["id"] = str(data["id"])
        return data


class UserMongo(UserBase, Document): ...


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
            }
        }
    )
