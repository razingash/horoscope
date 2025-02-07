from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_session
from apps.moon.crud import get_moon_phases_with_events
from apps.moon.schemas import MoonPhasesResponse

router = APIRouter()

@router.get(path="/lunar-forecast/{year}/")#, response_model=MoonPhasesResponse) # for current location (permalink)
async def get_moon_info(year: int, session: AsyncSession = Depends(db_session.session_dependency)):
    """now timezone is UTC"""
    phases = await get_moon_phases_with_events(session=session, year=year)
    return phases

