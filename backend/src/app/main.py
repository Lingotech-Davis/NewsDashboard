# from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.config import Settings, get_settings
from src.db import models
from src.db.database import engine
from src.router.db import db_router
from src.router.news import news_router
from src.router.bias import bias_router
from src.router.rag import rag_router
from src.router.summarize import summarize_router

# Setting Atttributes
# Attributes:
#     GEMINI_API_KEY: str
#     NEWS_API_KEY: str
#     DB_USER: str
#     DB_PASSWORD: str
#     DB_NAME: str


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "http://localhost:3000",  # Front end
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news_router, prefix="/api/v1/news")
app.include_router(db_router, prefix="/api/v1/db")
app.include_router(bias_router, prefix="/api/v1/bias")
app.include_router(rag_router, prefix="/api/v1/rag")
app.include_router(summarize_router, prefix="/api/v1/summarize")


@app.get("/ping/")
async def ping():
    return {"message": "pong"}


# TODO: REMOVE FOR DEPLOYMENT
@app.get("/env-check")  # ENV IS WORKING :)
async def env_check(settings: Annotated[Settings, Depends(get_settings)]):
    return settings
