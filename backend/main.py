"""requirements.txt
fastapi
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI

from config import Settings

app = FastAPI()


@lru_cache
def get_settings():
    """
    Loads API keys
    To access afterwards, call similar to below. (The Depends is a FastAPI function to manage dependencies)
    Attributes:
        GEMINI_API_KEY: str
        NEWS_API_KEY: str
        POSTGRESQL_PWD: str
    """
    # returns settings object
    return Settings()  # type: ignore (making linter shut up)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/env-check")  # ENV IS WORKING :)
async def env_check(settings: Annotated[Settings, Depends(get_settings)]):
    return settings


@app.get("/users/{user_id}/items/{item_id}")  # Example of path parameters
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
