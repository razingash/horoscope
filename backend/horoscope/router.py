from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_session

router = APIRouter()

@router.get(path='/daily/')
async def get_daily_horoscope(session: AsyncSession = Depends(db_session.session_dependency)):
    #horoscope = await get_horoscope_
    return {'horoscope': 'horoscope'}

