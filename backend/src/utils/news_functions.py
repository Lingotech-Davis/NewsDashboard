"""requirements.txt
requests
### IMPORTANT: download in the following order: 1) lxml -> 2) newspaper3k
# Otherwise errors crop up
lxml_html_clean
newspaper3k
"""

import logging

import asyncio
import httpx
import requests
from newspaper import Article
from newspaper.article import ArticleException

logger = logging.getLogger(__name__)


def call_news_api(keyword, date, NEWS_API_KEY, everything=True):
    API_KEY = NEWS_API_KEY

    # choose endpoint
    endpoint = "everything" if everything else "top-headlines"
    # build URL with the passed-in variables

    url = (
        f"https://newsapi.org/v2/{endpoint}"
        f"?q={keyword}"
        f"&from={date}"
        "&sortBy=relevancy"
        f"&apiKey={API_KEY}"
    )
    response = requests.get(url)
    return response


async def query_news_api(
    client: httpx.AsyncClient,
    keyword: str,
    NEWS_API_KEY: str,
    everything: bool = True,
    sortBy: str = None,
):
    """
    Asynchronously queries the News API using httpx.
    """
    endpoint = "everything" if everything else "top-headlines"
    assert sortBy in ["relevancy", "popularity", "publishedAt", None]
    sortString = f"&sortBy={sortBy}" if (sortBy and endpoint == "everything") else ""
    pageSizeDefault = 20

    url = (
        f"https://newsapi.org/v2/{endpoint}"
        f"?q={keyword}"
        f"&apiKey={NEWS_API_KEY}"
        f"&pageSize={pageSizeDefault}" + sortString
    )
    # Use the async client to make a non-blocking request
    response = await client.get(url)
    return response


def _extract_newspaper_contents_sync(article_url: str):
    """
    Synchronously downloads and parses an article using the newspaper3k library.
    This is a blocking function.
    """
    article = Article(article_url)
    try:
        # The .download() method is a blocking operation.
        article.download()
        article.parse()

        text = article.text
        title = article.title
        filtered_lines = filter(str.strip, text.splitlines())
        cleaned_text = "\n".join(filtered_lines)
        return {"title": title, "text": cleaned_text}

    except ArticleException as e:
        logger.debug(f"Error on URL: {article_url} - {e}")
        return None


async def extract_newspaper_contents(article_url: str):
    """
    Asynchronously extracts article content by running the synchronous
    scraping logic on a separate thread using asyncio.to_thread.
    """
    return await asyncio.to_thread(_extract_newspaper_contents_sync, article_url)
