from datetime import datetime

from sqlalchemy.orm import Session

from core.models import HoroscopePatterns
from services.horoscope.natal_chart import calculate_transits_for_natal_chart, calculate_aspects_for_natal_chart


async def get_horoscope_for_one_day(session: Session): # ! позже кэшировать результат
    date = datetime.today()
    year, month, day = date.year, date.month, date.day

    transits = await calculate_transits_for_natal_chart(date, date)
    aspects = calculate_aspects_for_natal_chart(transits)

    horoscope = []
"""
    for zodiac in range(1, 12):
        horoscope_patterns = session.query(HoroscopePatterns).filter(
            HoroscopePatterns.language == "ru",
            HoroscopePatterns.zodiac == zodiac,
            HoroscopePatterns.planet == planet,
            HoroscopePatterns.house == house,
            HoroscopePatterns.aspect == aspect
        )
"""

