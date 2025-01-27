from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_session
from core.models import LanguagesChoices
from horoscope.crud import get_horoscope_daily, get_horoscope_annual, get_horoscope_monthly, get_horoscope_weekly

router = APIRouter()

@router.get(path='/daily/')
async def get_daily_horoscope(
        date: datetime = Query(default=datetime.now(timezone.utc)),
        language: LanguagesChoices = Query(default=LanguagesChoices.ENGLISH),
        session: AsyncSession = Depends(db_session.session_dependency)
):
    horoscope = await get_horoscope_daily(session=session, date=date, language=language)
    return horoscope


@router.get(path='/weekly/')
async def get_monthly_horoscope(
        date: datetime = Query(default=datetime.now(timezone.utc)),
        language: LanguagesChoices = Query(default=LanguagesChoices.ENGLISH),
        session: AsyncSession = Depends(db_session.session_dependency)
):
    horoscope = await get_horoscope_weekly(session=session, date=date, language=language)
    return horoscope


@router.get(path='/monthly/')
async def get_monthly_horoscope(
        date: datetime = Query(default=datetime.now(timezone.utc)),
        language: LanguagesChoices = Query(default=LanguagesChoices.ENGLISH),
        session: AsyncSession = Depends(db_session.session_dependency)
):
    horoscope = await get_horoscope_monthly(session=session, date=date, language=language)
    return horoscope


@router.get(path='/annual/')
async def get_annual_horoscope(
        date: datetime = Query(default=datetime.now(timezone.utc)),
        language: LanguagesChoices = Query(default=LanguagesChoices.ENGLISH),
        session: AsyncSession = Depends(db_session.session_dependency)
):
    horoscope = await get_horoscope_annual(session=session, date=date, language=language)
    return horoscope
