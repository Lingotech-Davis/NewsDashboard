import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import TIMESTAMP, UUID, Column, String, text

from src.db.database import Base


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
