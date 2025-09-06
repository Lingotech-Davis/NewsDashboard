import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db import models, schemas
from src.db.database import get_db

db_router = APIRouter()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@db_router.get("/read-db-chunks/", response_model=list[schemas.ChunkRead])
async def read_db_chunks(db: Session = Depends(get_db)):
    """
    Retrieves all chunk entries from the database.
    """
    logger.info("Reading DB Chunks")
    entries = db.query(models.Chunk).all()
    return [schemas.ChunkRead.model_validate(entry) for entry in entries]


@db_router.get(
    "/read-db-articles/", response_model=list[schemas.ArticleReadNoEmbeddings]
)
async def read_db_articles(db: Session = Depends(get_db)):
    """
    Retrieves all article entries from the database.
    """
    logger.info("Reading DB Articles")
    entries = db.query(models.Article).all()
    return [schemas.ArticleReadNoEmbeddings.model_validate(entry) for entry in entries]
