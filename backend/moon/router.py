from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_session
from services.moon.services import get_moon_phases

router = APIRouter()

@router.get(path="/lunar-forecast/{year}/{month}") # for current location (permalink)
async def get_moon_info_by_timezone(year: int, month: int, session: AsyncSession = Depends(db_session.session_dependency)):
    phases = await get_moon_phases(session=session, year=year, month=month)
    return {'moon phases': phases}

@router.get(path="/lunar-forecast")
async def get_test_info():
    return {'info': 'test info'}
