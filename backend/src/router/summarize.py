from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.utils.summarization import (
    summarize_nlp, summarize_generate
)
from src.utils.bias_detection import (
    NewsScrape,
)
from src.config.config import get_settings

from typing import Optional, Dict
import json

# Initialize router
summarize_router = APIRouter()

# Define request schema
class SummaryURL(BaseModel):
    url: Optional[str] = None
    sentences: Optional[int] = None
    query: Optional[str] = None

@summarize_router.post("/analyze")
def summarize_article(input: SummaryURL):

    # Step 0: Initialize
    url = input.url or None
    sentences = input.sentences or None

    # Step 1: Ensure correct usage
    if not (url and sentences):
       print("Bad URL or bad num_sentences")
       return None

    # Step 2: Scrape and summarize
    article = NewsScrape(url)
    text = article['text']
    summary = summarize_nlp(text, sentences)

    # Step 3: Return response ['title', 'authors', 'publish_date', 'text', 'source']
    response = {
        "summary": summary,
        "extra": {
           "title": article['title'],
           "authors": article['authors'],
           "publish_date": article['publish_date'],
           "text": article['text'],
           "source": article['source'],
        }
    }
    print("Debug:\n", json.dumps(response, indent=2, default=str))
    return response

@summarize_router.post("/generate")
def generate_summary(input: SummaryURL):

    # Step 0: Initialize
    url = input.url or None
    sentences = input.sentences or None

    # Step 1: Ensure correct usage
    if not (url and sentences):
        print("Bad URL or bad num_sentences")
        return None

    # Step 2: Scrape and summarize
    settings = get_settings()
    article = NewsScrape(url)
    text = article['text']
    summary = summarize_generate(text, sentences, settings.GEMINI_API_KEY)

    # Step 3: Return response
    response = {
        "summary": summary,
        "extra": {
           "title": article['title'],
           "authors": article['authors'],
           "publish_date": article['publish_date'],
           "text": article['text'],
           "source": article['source'],
        }
    }
    print("Debug:\n", json.dumps(response, indent=2, default=str))
    return response