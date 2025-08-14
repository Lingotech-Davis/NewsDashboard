import logging
from typing import Annotated

import requests
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.config import Settings, get_settings
from src.db import models, schemas
from src.db.database import get_db

db_router = APIRouter()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@db_router.get("/read-db/")
async def read_db(db: Session = Depends(get_db)):
    logger.info("Reading DB")
    entries = db.query(models.Chunk).all()
    return entries
