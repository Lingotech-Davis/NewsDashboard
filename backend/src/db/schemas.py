import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


# Type declaration for newsAPI
class Source(BaseModel):
    """
    Represents the source of a news article.
    """

    id: Optional[str] = Field(
        None, description="The unique identifier for the news source."
    )
    name: str = Field(..., description="The name of the news source.")


class Article(BaseModel):
    """
    Represents a single news article.
    """

    source: Source = Field(..., description="The source of the article.")
    author: Optional[str] = Field(None, description="The author of the article.")
    title: str = Field(..., description="The title of the article.")
    description: Optional[str] = Field(
        None, description="A brief description of the article."
    )
    url: str = Field(..., description="The URL to the full article.")
    urlToImage: Optional[str] = Field(
        None, description="A URL to an image associated with the article."
    )
    publishedAt: datetime = Field(
        ...,
        description="The date and time the article was published (ISO 8601 format).",
    )
    content: Optional[str] = Field(None, description="The content of the article.")


class NewsApiResponse(BaseModel):
    """
    The top-level response structure for the news API.
    """

    status: str = Field(..., description="The status of the request (e.g., 'ok').")
    totalResults: int = Field(..., description="The total number of results found.")
    articles: List[Article] = Field(..., description="A list of news articles.")


class ArticleContentResponse(BaseModel):
    """Schema for a successful response with extracted article content."""

    title: str = Field(..., description="The title of the article.")
    text: str = Field(..., description="The cleaned, extracted text of the article.")
