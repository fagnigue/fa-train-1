
from app.database.base import SessionLocal


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()