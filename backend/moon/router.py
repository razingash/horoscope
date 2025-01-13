from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_session
from moon.schemas import MoonPhasesResponse
from services.moon.services import get_moon_phases

router = APIRouter()

@router.get(path="/lunar-forecast/{year}/{month}", response_model=MoonPhasesResponse) # for current location (permalink)
async def get_moon_info_by_timezone(year: int, month: int, session: AsyncSession = Depends(db_session.session_dependency)):
    """now timezone is UTC"""
    phases = await get_moon_phases(session=session, year=year, month=month)
    return {'moon phases': phases}

