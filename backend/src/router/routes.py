import logging
import re
from datetime import datetime, timedelta
from typing import Annotated, Dict

import requests
from fastapi import APIRouter, Depends, HTTPException, status

# Import the settings from the root of the 'src' package.
from src.config.config import Settings, get_settings
from src.db.schemas import ArticleContentResponse, NewsApiResponse, UrlPayload
from src.utils.news_functions import call_news_api, extract_newspaper_contents

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

    try:
        current_datetime = datetime.now()
        one_week_ago = current_datetime - timedelta(weeks=1)
        one_week_ago_date_only = one_week_ago.date()

        news_api_response = call_news_api(
            query, one_week_ago_date_only.isoformat(), settings.NEWS_API_KEY
        )
        logger.debug(f"Received response from News API: {news_api_response}")

    except requests.exceptions.HTTPError as err:
        # We catch the HTTPError and re-raise it as an HTTPException
        # with the appropriate status code.
        raise HTTPException(
            status_code=err.response.status_code,
            detail=f"External News API error: {err.response.text}",
        )
    except Exception as e:
        # A catch-all for any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )

    return news_api_response.json()


@router.get("/news-extract", response_model=ArticleContentResponse)
async def extract_news(
    payload: UrlPayload, settings: Annotated[Settings, Depends(get_settings)]
):
    extracted_content = extract_newspaper_contents(payload.story_url)

    if not extracted_content:
        logger.error(f"Failed to extract content from {payload.story_url}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to extract content from URL. The site may be blocking bots.",
        )

    title, text = extracted_content["title"], extracted_content["text"]
    # TODO: Modify the utility function to return both title and text.
    return ArticleContentResponse(title=title, text=text)
