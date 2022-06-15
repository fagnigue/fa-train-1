
from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from app.database.getdb import getDb
from app.models.user import User
from app.schemas import user as userSchema
from app.services import user as userService
from app.services import common as commonService


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def createUser(data: userSchema.UserCreate, db: Session = Depends(getDb)) -> User:
    userUnique = {
        "id": None,
        "email": data.email
    }
    user = userService.getUser(db, userUnique)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return userService.createUser(db, data)



@router.get("/")
def listUser(
    skip: Union[int, None] = Query(0),
    limit: Union[int, None] = Query(100),
    db: Session = Depends(getDb),
    ) -> list[User]:
    return userService.getUsers(db, skip, limit)



@router.get("/{userId}")
def getUser(
    userId: str = Path(...),
    db: Session = Depends(getDb)
) -> User:
    userUnique = {
            'id': userId if commonService.isValidUUID(userId) else None,
            'email': userId
        }
    return userService.getUser(db, userUnique)
