from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.horoscope.schemas import HoroscopeQueryParams
from core.database import db_session
from apps.horoscope.crud import get_horoscope_daily, get_horoscope_annual, get_horoscope_monthly, get_horoscope_weekly

router = APIRouter()

@router.get(path='/daily/')
async def get_daily_horoscope(
        params: HoroscopeQueryParams = Depends(),
        session: AsyncSession = Depends(db_session.session_dependency)
):
    horoscope = await get_horoscope_daily(session=session, date=params.date, language=params.language)
    return horoscope


@router.get(path='/weekly/')
async def get_monthly_horoscope(
        params: HoroscopeQueryParams = Depends(),
        session: AsyncSession = Depends(db_session.session_dependency)
):
    horoscope = await get_horoscope_weekly(session=session, date=params.date, language=params.language)
    return horoscope


@router.get(path='/monthly/')
async def get_monthly_horoscope(
        params: HoroscopeQueryParams = Depends(),
        session: AsyncSession = Depends(db_session.session_dependency)
):
    horoscope = await get_horoscope_monthly(session=session, date=params.date, language=params.language)
    return horoscope


@router.get(path='/annual/')
async def get_annual_horoscope(
        params: HoroscopeQueryParams = Depends(),
        session: AsyncSession = Depends(db_session.session_dependency)
):
    horoscope = await get_horoscope_annual(session=session, date=params.date, language=params.language)
    return horoscope
