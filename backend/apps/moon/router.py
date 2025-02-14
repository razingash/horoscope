from fastapi import APIRouter, Depends
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_session
from apps.moon.crud import get_moon_phases_with_events\

router = APIRouter()

@router.get(path="/lunar-forecast/{year}/")
async def get_moon_info(
        year: int = Path(..., ge=1550, le=2650),
        session: AsyncSession = Depends(db_session.session_dependency)
):
    """now timezone is UTC"""
    phases = await get_moon_phases_with_events(session=session, year=year)
    return phases

