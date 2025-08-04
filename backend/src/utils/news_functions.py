"""requirements.txt
requests
### IMPORTANT: download in the following order: 1) lxml -> 2) newspaper3k
# Otherwise errors crop up
lxml_html_clean
newspaper3k
"""

import requests

# from newspaper import Article
# from newspaper.article import ArticleException


def call_news_api(keyword, date, NEWS_API_KEY, everything=True):

    # choose endpoint
    endpoint = "everything" if everything else "top-headlines"
    # build URL with the passed-in variables
    url = (
        f"https://newsapi.org/v2/{endpoint}"
        f"?q={keyword}"
        f"&from={date}"
        "&sortBy=relevancy"
        f"&apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)
    if not response.ok:
        return False
    return response.json()
