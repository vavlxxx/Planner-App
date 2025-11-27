import sys
from pathlib import Path
from contextlib import asynccontextmanager

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
from src.routes.users import user_router
from src.routes.events import event_router
from src.database.connection import conn
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    conn()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        # host="0.0.0.0", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
    )
