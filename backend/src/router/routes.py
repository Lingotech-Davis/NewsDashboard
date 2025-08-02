from typing import Annotated, Dict

from fastapi import APIRouter, Depends

# Import the settings from the root of the 'src' package.
from src.config.config import Settings, get_settings

router = APIRouter()


@router.get("/env-check")  # ENV IS WORKING :)
async def env_check(settings: Annotated[Settings, Depends(get_settings)]):
    return settings
