from fastapi import FastAPI
from app.database.base import engine
from app.database.base import Base
from app.routers import user, post

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FA-TRAIN-1", version="1.0.0")

app.include_router(user.router)
app.include_router(post.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

