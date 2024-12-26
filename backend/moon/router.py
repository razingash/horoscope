from datetime import datetime

from fastapi import APIRouter

from services.moon.services import get_moon_phases

router = APIRouter()

@router.get(path="/lunar-forecast/{year}/{month}") # for current location (permalink)
async def get_moon_info_by_timezone(year: int, month: int):
    phases = get_moon_phases(date=datetime(year, month, 1))
    return {'moon phases': phases}

