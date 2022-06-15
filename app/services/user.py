from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models import user as userModel
from app.schemas import user as userSchema
import bcrypt
import copy

def getUser(db: Session, userUnique: userSchema.UserUnique) -> userModel.User:
    print(userUnique)
    user = db.query(userModel.User).filter(
        or_(
            userModel.User.id == userUnique["id"],
            userModel.User.email == userUnique["email"]
            )
    ).first()
    if user is not None:
        user = user.__dict__
        del user["password"]
    return user


def getUsers(db: Session, skip: int=0, limit: int = 100) -> list[userModel.User]:
    users = db.query(userModel.User).offset(skip).limit(limit).all()
    for user in users:
        del user.password
    return users


def createUser(db: Session, data: userSchema.UserCreate) -> userModel.User:
    salt = bcrypt.gensalt()
    clearPassword = copy.copy(data.password).encode('UTF-8')
    data.password = bcrypt.hashpw(clearPassword, salt)
    user = userModel.User(**data.dict())
    user.is_verified = False
    db.add(user)
    db.commit()
    db.refresh(user)

    del user.password
    return user
