"""requirements.txt
requests
### IMPORTANT: download in the following order: 1) lxml -> 2) newspaper3k
# Otherwise errors crop up
lxml_html_clean
newspaper3k
"""

import logging

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


def extract_newspaper_contents(article_url):
    """
    given a url to some article, return its content
    this is really just a helper function. also has safeguards for articles that block the scraping tool.
    """
    article = Article(article_url)
    try:
        article.download()
        article.parse()

        # cleaning it up
        text = article.text
        title = article.title
        filtered_lines = filter(str.strip, text.splitlines())
        cleaned_text = "\n".join(filtered_lines)
        return {"title": title, "text": cleaned_text}

    except ArticleException as e:
        logger.debug(
            f"Error on following url: rejected request or malformed url? - {article_url} - {e}"
        )
        return None
