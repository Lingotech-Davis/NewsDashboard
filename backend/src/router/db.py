import logging
from typing import Annotated

import asyncio
import requests
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from newspaper.article import ArticleException
import httpx

from src.config.config import Settings, get_settings
from src.db import models, schemas
from src.db.schemas import ChunkRead
from src.db.database import get_db
from src.utils.news_functions import query_news_api, extract_newspaper_contents
from src.utils.database import filter_out_existing_articles, store_articles
from src.utils.local_models import (
    # get_keybert_model,
    # extract_main_keyword,
    get_embeddings_model,
    add_embeddings,
    chunkify,
)

db_router = APIRouter()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@db_router.get("/read-db/")
async def read_db(db: Session = Depends(get_db)):
    logger.info("Reading DB")
    entries = db.query(models.Chunk).all()
    return [ChunkRead.model_validate(entry) for entry in entries]


async def scrape_and_embed_article(article_data: dict, model):
    """
    Asynchronously scrapes, chunks, and embeds a single article.
    """
    try:
        # Use httpx for async requests
        article_content_dict = await extract_newspaper_contents(article_data["url"])

        if not article_content_dict:
            article_data["text"] = article_data.get("content", "")
            article_data["scrape_successful"] = False
        else:
            article_data["text"] = article_content_dict.get("text", "")
            article_data["scrape_successful"] = True

    except Exception as e:
        # Handle scraping errors gracefully without stopping the entire process
        print(f"Error scraping {article_data.get('url')}: {e}")
        article_data["text"] = article_data.get("content", "")
        article_data["scrape_successful"] = False

    # Chunk and embed the content
    chunk_list = chunkify(article_data.get("text", ""))
    embeddings_list = add_embeddings(chunk_list, model)

    # Attach the processed data to the article dictionary
    article_data["chunks"] = chunk_list
    article_data["embeddings_list"] = embeddings_list

    return article_data


@db_router.post("/store-query/")
async def store_query(
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[Session, Depends(get_db)],
    query: str = "stock",
):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            news_api_response = await query_news_api(
                client, query, settings.NEWS_API_KEY
            )
            news_api_response.raise_for_status()
        # Use httpx for async requests
    except httpx.HTTPStatusError as err:
        raise HTTPException(
            status_code=err.response.status_code,
            detail=f"External News API error: {err.response.text}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )

    news_api_data = news_api_response.json()
    articles_to_scrape = filter_out_existing_articles(
        news_api_data.get("articles", []), db
    )

    # Transform the data from the News API response
    article_properties = [
        "url",
        "urlToImage",
        "source",
        "author",
        "title",
        "description",
        "publishedAt",
        "content",
    ]
    articles_to_embed = []
    for article in articles_to_scrape:
        to_embed = {}
        for prop in article_properties:
            if prop == "source":
                to_embed["source"] = article.get("source", {}).get("name")
            else:
                to_embed[prop] = article.get(prop)
        articles_to_embed.append(to_embed)

    MiniLM = get_embeddings_model()

    # Use asyncio.gather to process all articles concurrently
    processed_articles = await asyncio.gather(
        *[scrape_and_embed_article(article, MiniLM) for article in articles_to_embed]
    )

    # Call the storage function just once with the list of processed articles.
    store_articles(processed_articles, db)

    return {
        "message": f"Successfully processed and stored {len(processed_articles)} articles."
    }
