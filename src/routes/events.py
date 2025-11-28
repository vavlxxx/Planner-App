from typing import List

from fastapi import APIRouter, Body, HTTPException, status
from beanie import PydanticObjectId

from routes.dependencies import EventDB
from src.models.events import Event, EventBase, EventMongo, EventUpdate
from src.models.users import UserMongo

event_router = APIRouter(tags=["Events"])


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(event_database: EventDB) -> List[Event]:
    events = await event_database.get_all()
    return [Event(**event.model_dump()) for event in events]


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId, event_database: EventDB) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist",
        )
    return Event(**event.model_dump())


@event_router.post("/new")
async def create_event(event_database: EventDB, body: EventBase = Body(...)):
    body_ = body.model_dump()
    if not body_.get("user_id", None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Provide 'user_id' field in the body",
        )

    user = await UserMongo.find_one(
        UserMongo.id == PydanticObjectId(body_.get("user_id"))
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID does not exist",
        )

    doc = EventMongo(**body_)
    event = await event_database.save(doc)
    return Event(**event.model_dump())


@event_router.put("/{id}", response_model=Event)
async def update_event(
    id: PydanticObjectId, event_database: EventDB, body: EventUpdate
) -> Event:
    if body.user_id:
        user = await UserMongo.find_one(UserMongo.id == PydanticObjectId(body.user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with supplied ID does not exist",
            )

    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist",
        )
    return Event(**updated_event.model_dump())


@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId, event_database: EventDB) -> dict:
    event = await event_database.delete(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist",
        )
    return {"message": "Event deleted successfully."}
