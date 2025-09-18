from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


# Type declaration for newsAPI article source
class Source(BaseModel):
    """
    Represents the source of a news article.
    """

    id: Optional[str] = Field(
        None, description="The unique identifier for the news source."
    )
    name: str = Field(..., description="The name of the news source.")


# NewsApi article structure, referenced below
class ArticleResponse(BaseModel):
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


# schema for NewsApi response structure
class NewsApiResponse(BaseModel):
    """
    The top-level response structure for the news API.
    """

    status: str = Field(..., description="The status of the request (e.g., 'ok').")
    totalResults: int = Field(..., description="The total number of results found.")
    articles: List[ArticleResponse] = Field(..., description="A list of news articles.")


# response schema for article scrape success
class ArticleContentResponse(BaseModel):
    """Schema for a successful response with extracted article content."""

    title: str = Field(..., description="The title of the article.")
    text: str = Field(..., description="The cleaned, extracted text of the article.")


class ChunkRead(BaseModel):
    """
    Pydantic model for reading Chunk data.
    This schema reflects the current structure of the Chunk SQLAlchemy model.
    """

    chunk_id: UUID
    content: str
    embedding: List[float]
    created_at: datetime
    article_id: UUID

    model_config = ConfigDict(from_attributes=True)


# Used for Chunk read routes and for first draft of RAG rotue
class ChunkReadNoEmbedding(BaseModel):
    """
    Pydantic model for reading Chunk data.
    This schema reflects the current structure of the Chunk SQLAlchemy model.
    """

    chunk_id: UUID
    content: str
    created_at: datetime
    article_id: UUID

    model_config = ConfigDict(from_attributes=True)


# Base class of properties
class ArticleBase(BaseModel):
    """
    Pydantic base model for Article data.
    """

    url: str
    urlToImage: Optional[str] = None
    source: Optional[str] = None
    author: Optional[str] = None
    title: str
    description: Optional[str] = None
    publishedAt: datetime
    scrape_successful: str
    text: str


class ArticleCreate(ArticleBase):
    pass


# Article declaration including related chunks
class Article(ArticleBase):
    """
    Pydantic model for a complete Article with its chunks.
    """

    article_id: UUID
    chunks: List[ChunkRead] = []

    model_config = ConfigDict(from_attributes=True)


# Used for Article read routes (in order to not get Chunks and their embeddings)
class ArticleReadNoEmbeddings(ArticleBase):
    """
    Pydantic model for an article without linking its chunks
    """

    article_id: UUID

    model_config = ConfigDict(from_attributes=True)


# Used for RAG routes, includes article name and image URL for display purposes
class ArticleRagRead(BaseModel):
    url: str
    urlToImage: Optional[str] = None
    source: Optional[str] = None
    author: Optional[str] = None
    title: str
    publishedAt: datetime

    model_config = ConfigDict(from_attributes=True)


class ChunkReadWithArticleInfo(ChunkReadNoEmbedding):
    article: ArticleRagRead

    model_config = ConfigDict(from_attributes=True)


class RagResponse(BaseModel):
    articles: List[ArticleRagRead]
    gemini_response: str
