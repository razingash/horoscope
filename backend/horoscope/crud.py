from datetime import datetime, timezone

from skyfield.api import load
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from commands.postinitialization import get_daily_horoscope_descriptions, get_weekly_horoscope_descriptions, \
    get_monthly_horoscope_descriptions, get_annual_horoscope_descriptions
from core.models import HoroscopeDaily, LanguagesChoices, HoroscopeWeekly, HoroscopeMonthly, ZodiacsChoices, \
    HoroscopeTypes, HoroscopeAnnual
from horoscope.utils import get_season
from services.horoscope.prediction import get_week_number, generate_horoscope

"""
кэшировать апи для этого проиложения на уровне Nginx используя json и временные зоны
"""
"""! отправлять текущую дату и временную зону с фронта чтобы не быть подвязанным под сервер
!! надо будет тогда сделать проверку, чтобы дата была в пределах +- 1, чтобы нельзя было спарсить все наперед
"""

ts = load.timescale()
now = datetime.now(timezone.utc)
start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
start_date = ts.utc(start_date)

language = LanguagesChoices.russian
year, month, day = now.year, now.month, now.day

async def get_horoscope_daily(session: AsyncSession):
    query = await session.execute(select(HoroscopeDaily.zodiac, HoroscopeDaily.description).where(
        HoroscopeDaily.language == language,
        HoroscopeDaily.year == year,
        HoroscopeDaily.month == month,
        HoroscopeDaily.day == day,
    ))
    rows = query.fetchall()

    if not rows:
        data = generate_horoscope(horoscope_type=HoroscopeTypes.DAILY, start_date=start_date)

        horoscope_descriptions = await get_daily_horoscope_descriptions(session, data)
        await save_horoscope_data(session, HoroscopeDaily, horoscope_descriptions, day=day, month=month, year=year)

        horoscope_data = horoscope_descriptions[language]
    else:
        horoscope_data = {zodiac: description for zodiac, description in rows}

    return horoscope_data


async def get_horoscope_weekly(session: AsyncSession):
    week_number = get_week_number(year, month, day)
    query = await session.execute(select(HoroscopeWeekly.zodiac, HoroscopeWeekly.description).where(
        HoroscopeWeekly.language == language,
        HoroscopeWeekly.year == year,
        HoroscopeWeekly.month == month,
        HoroscopeWeekly.week_number == week_number,
    ))
    rows = query.fetchall()

    if not rows:
        data = generate_horoscope(horoscope_type=HoroscopeTypes.WEEKLY, start_date=start_date)

        horoscope_descriptions = await get_weekly_horoscope_descriptions(session, choosen_date=now, data=data)
        await save_horoscope_data(session, HoroscopeWeekly, horoscope_descriptions,
                                  week_number=week_number, month=month, year=year)

        horoscope_data = horoscope_descriptions[language]
    else:
        horoscope_data = {zodiac: description for zodiac, description in rows}

    return horoscope_data


async def get_horoscope_monthly(session: AsyncSession):
    query = await session.execute(select(HoroscopeMonthly.zodiac, HoroscopeMonthly.description).where(
        HoroscopeMonthly.language == language,
        HoroscopeMonthly.year == year,
        HoroscopeMonthly.month == month,
    ))
    rows = query.fetchall()

    if not rows:
        data = generate_horoscope(horoscope_type=HoroscopeTypes.MONTHLY, start_date=start_date)

        season = get_season(month=month)
        horoscope_descriptions = await get_monthly_horoscope_descriptions(session, data=data, season=season)
        await save_horoscope_data(session, HoroscopeMonthly, horoscope_descriptions, month=month, year=year)

        horoscope_data = horoscope_descriptions[language]
    else:
        horoscope_data = {zodiac: description for zodiac, description in rows}

    return horoscope_data


async def get_horoscope_annual(session: AsyncSession):
    query = await session.execute(select(HoroscopeAnnual.zodiac, HoroscopeAnnual.description).where(
        HoroscopeAnnual.language == language,
        HoroscopeAnnual.year == year,
    ))
    rows = query.fetchall()

    if not rows:
        data = generate_horoscope(horoscope_type=HoroscopeTypes.ANNUAL, start_date=start_date)

        horoscope_descriptions = await get_annual_horoscope_descriptions(session, data=data)
        await save_horoscope_data(session, HoroscopeAnnual, horoscope_descriptions, year=year)

        horoscope_data = horoscope_descriptions[language]
    else:
        horoscope_data = {zodiac: description for zodiac, description in rows}

    return horoscope_data


async def save_horoscope_data(session, model_class, data, **kwargs):
    """сохраняет поулченные данные для гороскопа в базу данных"""
    for language in LanguagesChoices:
        language = language.value
        for zodiac in ZodiacsChoices:
            zodiac = zodiac.value
            description = data[language][zodiac]
            filters = dict(language=language, zodiac=zodiac, **kwargs)
            horoscope = model_class(description=description, **filters)
            session.add(horoscope)
    await session.commit()
