from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlmodel import select

from src.database.connection import get_session
from src.database.models import User, UserSignIn, UserUpdate, UserRead


user_router = APIRouter(
    tags=["User"]
)


@user_router.post("/signup")
async def sign_new_user(data: User, session=Depends(get_session)) -> dict:
    statement = select(User).where(User.email == data.email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied email already exists"
        )
    
    session.add(data)
    session.commit()
    session.refresh(data)
    
    return {
        "message": "User successfully registered!",
        "user_id": data.id
    }


@user_router.post("/signin")
async def sign_user_in(user: UserSignIn, session=Depends(get_session)) -> dict:
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()
    
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    
    if existing_user.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed"
        )
    
    return {
        "message": "User signed in successfully",
        "user_id": existing_user.id,
        "email": existing_user.email
    }


@user_router.get("/", response_model=List[UserRead])
async def retrieve_all_users(session=Depends(get_session)) -> List[User]:
    statement = select(User)
    users = session.exec(statement).all()
    return users


@user_router.get("/{id}", response_model=UserRead)
async def retrieve_user(id: int, session=Depends(get_session)) -> User:
    user = session.get(User, id)
    if user:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User with supplied ID does not exist"
    )


@user_router.put("/edit/{id}", response_model=UserRead)
async def update_user(
    id: int, 
    new_data: UserUpdate, 
    session=Depends(get_session)
) -> User:
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID does not exist"
        )
    
    user_data = new_data.model_dump(exclude_unset=True)
    
    if "email" in user_data:
        statement = select(User).where(User.email == user_data["email"], User.id != id)
        existing_user = session.exec(statement).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already taken by another user"
            )
    
    for key, value in user_data.items():
        setattr(user, key, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user


@user_router.delete("/{id}")
async def delete_user(id: int, session=Depends(get_session)) -> dict:
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID does not exist"
        )
    
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}


@user_router.delete("/")
async def delete_all_users(session=Depends(get_session)) -> dict:
    statement = select(User)
    users = session.exec(statement).all()
    
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found to delete"
        )
    
    for user in users:
        session.delete(user)
    
    session.commit()
    return {"message": f"All {len(users)} users deleted successfully"}
