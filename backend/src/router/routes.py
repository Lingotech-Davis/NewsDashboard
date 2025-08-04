import logging
from datetime import datetime, timedelta
from typing import Annotated, Dict

from fastapi import APIRouter, Depends

# Import the settings from the root of the 'src' package.
from src.config.config import Settings, get_settings
from src.db.schemas import NewsApiResponse
from src.utils.news_functions import call_news_api

router = APIRouter()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@router.get("/env-check")  # ENV IS WORKING :)
async def env_check(settings: Annotated[Settings, Depends(get_settings)]):
    return settings


# Usage: http://localhost:8000/api/v1/top-stories/?query=stocky or http://localhost:8000/api/v1/top-stories/
@router.get("/top-stories/", response_model=NewsApiResponse)
async def top_stories(
    settings: Annotated[Settings, Depends(get_settings)], query: str = "stock"
):
    # def call_news_api(keyword, date, NEWS_API_KEY, everything=True):
    # query = keyword if keyword else "stock"

    current_datetime = datetime.now()
    one_week_ago = current_datetime - timedelta(weeks=1)
    one_week_ago_date_only = one_week_ago.date()

    news_api_response = call_news_api(
        query, one_week_ago_date_only.isoformat(), settings.NEWS_API_KEY
    )
    logger.debug(f"Received response from News API: {news_api_response}")

    if not news_api_response:  # if it failed, and is returning error
        return {"status": 200, "totalResults": 0, "articles": []}
    return news_api_response


@router.get("/news-extract/{story_url}")
async def env_check(story_url, settings: Annotated[Settings, Depends(get_settings)]):
    return settings
