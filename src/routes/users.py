from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Request, status, Response

from src.models.events import Event, EventMongo
from src.database.connection import Database
from src.models.users import User, UserSignIn, UserMongo

user_database = Database(UserMongo)
user_router = APIRouter(tags=["User"])


@user_router.post("/signup")
async def sign_user_up(user: UserSignIn):
    user_exist = await UserMongo.find_one(UserMongo.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already.",
        )
    user = UserMongo(**user.model_dump())
    await user_database.save(user)
    return {"message": "User created successfully"}


@user_router.post("/signin")
async def sign_user_in(user: UserSignIn, response: Response) -> User:
    user = await UserMongo.find_one(UserMongo.email == user.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist.",
        )

    if user.password == user.password:
        response.set_cookie(key="user_id", value=str(user.id))
        events = await EventMongo.find(EventMongo.user_id == str(user.id)).to_list()
        events = [Event(**event.model_dump()) for event in events]
        return User(**user.model_dump(), events=events)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed.",
    )


@user_router.post("/me")
async def get_user_profile(request: Request) -> User:
    _id = request.cookies.get("user_id")
    user = await UserMongo.find_one(UserMongo.id == PydanticObjectId(_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You're not signed in" if not _id else "User does not exist",
        )
    events = await EventMongo.find(EventMongo.user_id == _id).to_list()
    events = [Event(**event.model_dump()) for event in events]
    return User(**user.model_dump(), events=events)
