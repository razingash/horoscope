from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_session
from horoscope.crud import get_horoscope_daily, get_horoscope_annual, get_horoscope_monthly, get_horoscope_weekly

router = APIRouter()

@router.get(path='/daily/')
async def get_daily_horoscope(session: AsyncSession = Depends(db_session.session_dependency)):
    horoscope = await get_horoscope_daily(session=session)
    return horoscope


@router.get(path='/weekly/')
async def get_monthly_horoscope(session: AsyncSession = Depends(db_session.session_dependency)):
    horoscope = await get_horoscope_weekly(session=session)
    return horoscope


@router.get(path='/monthly/')
async def get_monthly_horoscope(session: AsyncSession = Depends(db_session.session_dependency)):
    horoscope = await get_horoscope_monthly(session=session)
    return horoscope


@router.get(path='/annual/')
async def get_annual_horoscope(session: AsyncSession = Depends(db_session.session_dependency)):
    horoscope = await get_horoscope_annual(session=session)
    return horoscope
