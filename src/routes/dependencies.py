from typing import Annotated
from fastapi import Depends
from src.database.connection import Database
from src.models.events import EventMongo
from src.models.users import UserMongo


class ResolveDatabase:
    def __init__(self, model):
        self.model = model

    def __call__(self):
        return Database(self.model)


EventDB = Annotated[Database, Depends(ResolveDatabase(EventMongo))]
UserDB = Annotated[Database, Depends(ResolveDatabase(UserMongo))]
