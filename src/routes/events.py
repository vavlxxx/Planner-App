from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlmodel import select

from src.database.connection import get_session
from src.database.models import Event, EventUpdate, EventRead, User


event_router = APIRouter(
    tags=["Events"]
)


@event_router.get("/", response_model=List[EventRead])
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return events


@event_router.get("/{id}", response_model=EventRead)
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )


@event_router.post("/new", response_model=EventRead)
async def create_event(
    new_event: Event,
    session=Depends(get_session),
) -> Event:
    if new_event.user_id:
        user = session.get(User, new_event.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with supplied ID does not exist"
            )
    
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return new_event


@event_router.put("/edit/{id}", response_model=EventRead)
async def update_event(
    id: int, 
    new_data: EventUpdate, 
    session=Depends(get_session)
) -> Event:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    
    event_data = new_data.model_dump(exclude_unset=True)
    
    if "user_id" in event_data and event_data["user_id"]:
        user = session.get(User, event_data["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with supplied ID does not exist"
            )
    
    for key, value in event_data.items():
        setattr(event, key, value)
    
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@event_router.delete("/{id}")
async def delete_event(id: int, session=Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    
    session.delete(event)
    session.commit()
    return {"message": "Event deleted successfully"}


@event_router.delete("/")
async def delete_all_events(session=Depends(get_session)) -> dict:
    statement = select(Event)
    events = session.exec(statement).all()
    
    if not events:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No events found to delete"
        )
    
    for event in events:
        session.delete(event)
    
    session.commit()
    return {"message": f"All {len(events)} events deleted successfully"}


@event_router.get("/user/{user_id}", response_model=List[EventRead])
async def retrieve_user_events(user_id: int, session=Depends(get_session)) -> List[Event]:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID does not exist"
        )
    
    statement = select(Event).where(Event.user_id == user_id)
    events = session.exec(statement).all()
    return events
