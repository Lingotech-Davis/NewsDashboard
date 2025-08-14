import logging
import re
from datetime import datetime, timedelta
from typing import Annotated

import requests
from fastapi import APIRouter, Depends, HTTPException, status

from src.config.config import Settings, get_settings
from src.db.schemas import ArticleContentResponse, NewsApiResponse
from src.utils.news_functions import call_news_api, extract_newspaper_contents

news_router = APIRouter()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# REMOVE FOR DEPLOYMENT
# @router.get("/env-check")  # ENV IS WORKING :)
# async def env_check(settings: Annotated[Settings, Depends(get_settings)]):
#     return settings


# Usage: http://localhost:8000/api/v1/top-stories/?query=stocky or http://localhost:8000/api/v1/top-stories/
@news_router.get("/top-stories/", response_model=NewsApiResponse)
async def top_stories(
    settings: Annotated[Settings, Depends(get_settings)], query: str = "stock"
):
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
        raise HTTPException(
            status_code=err.response.status_code,
            detail=f"External News API error: {err.response.text}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )

    return news_api_response.json()


# TODO: Review the story_url arg. Should it have default?
@news_router.get("/news-extract", response_model=ArticleContentResponse)
async def extract_news(
    story_url: str = "https://www.livescience.com/animals/land-mammals/virginia-opossums-the-american-marsupials-that-have-barely-changed-since-the-time-of-the-dinosaurs",
):
    # Django URL parse regex
    rough_url_validator = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    if not re.match(rough_url_validator, story_url):  # 422 error, bad URL
        logger.error(f"Received invalid URL: {story_url}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Received invalid URL format",
        )

    extracted_content = extract_newspaper_contents(story_url)

    if not extracted_content:  # 500 error, no content
        logger.error(f"Failed to extract content from {story_url}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to extract content from URL. The site may be blocking bots.",
        )

    title, text = extracted_content["title"], extracted_content["text"]
    return ArticleContentResponse(title=title, text=text)
