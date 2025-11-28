import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from src.routes.users import user_router
from src.routes.events import event_router
from src.models.events import EventMongo
from src.models.users import UserMongo

_MONGO_DETAILS = "mongodb://nefedov_mongo_db:27017/"


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.client = AsyncIOMotorClient(_MONGO_DETAILS)

    await init_beanie(
        database=app.client["events"],
        document_models=[UserMongo, EventMongo],
    )

    try:
        yield
    finally:
        app.client.close()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
