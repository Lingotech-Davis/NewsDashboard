# from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI

from src.config.config import Settings, get_settings
from src.db import models
from src.db.database import engine
from src.router.db import db_router
from src.router.news import news_router

# Setting Atttributes
# Attributes:
#     GEMINI_API_KEY: str
#     NEWS_API_KEY: str
#     DB_USER: str
#     DB_PASSWORD: str
#     DB_NAME: str


models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(news_router, prefix="/api/v1/news")
app.include_router(db_router, prefix="/api/v1/db")


@app.get("/ping/")
async def ping():
    return {"message": "pong"}


# TODO: REMOVE FOR DEPLOYMENT
@app.get("/env-check")  # ENV IS WORKING :)
async def env_check(settings: Annotated[Settings, Depends(get_settings)]):
    return settings
