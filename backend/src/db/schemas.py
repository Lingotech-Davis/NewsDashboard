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


class UrlPayload(BaseModel):
    """Schema for the request body containing the URL to scrape."""

    story_url: str = Field(..., description="The URL of the news article to extract.")

    @field_validator("story_url")
    def validate_url(cls, v):
        """Validates the URL using a regex before the route function is called."""
        rough_url_validator = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        if not re.match(rough_url_validator, v):
            raise ValueError("Invalid URL format.")
        return v


class ArticleContentResponse(BaseModel):
    """Schema for a successful response with extracted article content."""

    title: str = Field(..., description="The title of the article.")
    text: str = Field(..., description="The cleaned, extracted text of the article.")
