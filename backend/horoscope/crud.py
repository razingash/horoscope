from datetime import datetime, timezone, date

from skyfield.api import load
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import HoroscopePatterns, Horoscope
from services.horoscope.natal_chart import calculate_transits_for_natal_chart
from services.horoscope.prediction import generate_horoscope


async def get_horoscope_daily(session: AsyncSession): # ! позже кэшировать результат
    """! отправлять текущую дату и временную зону с фронта чтобы не быть подвязанным под сервер"""
    ts = load.timescale()
    start_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = ts.utc(start_date)

    transits = await calculate_transits_for_natal_chart(start_date=start_date, end_date=start_date)

    aspects = generate_horoscope(transits, horoscope_type=1)

    horoscope = {}
    print(aspects)
    """
    for zodiac in range(1, 12):
        horoscope_patterns = session.query(HoroscopePatterns).filter(
            HoroscopePatterns.language == "ru", # кастомное поле, задействовать после генерации всех предсказаний
            HoroscopePatterns.zodiac == zodiac,
            HoroscopePatterns.planet == planet,
            HoroscopePatterns.house == house,
            HoroscopePatterns.aspect == aspect
        )
    """
    return aspects


async def get_horoscope_annual(session: AsyncSession):
    ts = load.timescale()
    start_date = ts.utc(date(datetime.now().year, 1, 1))

    transits = await calculate_transits_for_natal_chart(start_date=start_date, end_date=start_date)

    data = generate_horoscope(transits, horoscope_type=4)

    print(data)

    return data
