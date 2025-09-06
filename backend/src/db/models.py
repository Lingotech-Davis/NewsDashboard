import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import TIMESTAMP, UUID, Column, String, text, ForeignKey
from sqlalchemy.orm import relationship

from src.db.database import Base


class Article(Base):
    """
    This model represents a single, unique news article.
    The `url` field has a uniqueness constraint to prevent
    the same article from being ingested multiple times.
    """

    __tablename__ = "articles"

    article_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String, unique=True, nullable=False, index=True)
    urlToImage = Column(String)
    source = Column(String)
    author = Column(String)
    title = Column(String)
    description = Column(String)
    publishedAt = Column(TIMESTAMP(timezone=True))
    scrape_successful = Column(String)
    text = Column(String)

    # Establishes a one-to-many relationship with the Chunk model.
    # 'back_populates' ensures a two-way link.
    chunks = relationship("Chunk", back_populates="article")


class Chunk(Base):
    """
    This model represents a single chunk of an article's content.
    It links back to the parent `Article` via a foreign key.
    """

    __tablename__ = "chunked_data"

    chunk_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String)
    embedding = Column(Vector(384))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    # Define the foreign key relationship to the Article model.
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.article_id"))

    # Establishes a many-to-one relationship with the Article model.
    # 'back_populates' creates the two-way link.
    article = relationship("Article", back_populates="chunks")


"""
Old Def
class Chunk(Base):
    __tablename__ = "chunked_data"

    chunk_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author = Column(String)
    url = Column(String)
    title = Column(String)
    source = Column(String)
    content = Column(String)
    embedding = Column(Vector(384))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
"""
