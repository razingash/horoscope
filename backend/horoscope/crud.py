from datetime import datetime, timezone, date

from skyfield.api import load
from sqlalchemy.ext.asyncio import AsyncSession

from horoscope.utils import get_season, get_current_lunar_phase
from services.horoscope.natal_chart import calculate_transits_for_natal_chart
from services.horoscope.prediction import generate_horoscope


async def get_horoscope_daily(session: AsyncSession): # ! позже кэшировать результат
    """! отправлять текущую дату и временную зону с фронта чтобы не быть подвязанным под сервер
    !! надо будет тогда сделать проверку, чтобы дата была в пределах +- 1, чтобы нельзя было спарсить все наперед
    """
    ts = load.timescale()
    start_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = ts.utc(start_date)

    transits = await calculate_transits_for_natal_chart(start_date=start_date, end_date=start_date)

    data = generate_horoscope(transits, horoscope_type=1)

    return data


async def get_horoscope_weekly(session: AsyncSession):
    ts = load.timescale()
    now = datetime.now()
    year, month, day = now.year, now.month, now.day
    #first_day_of_month = datetime(now.year, now.month, 1)
    #week_number_of_month = (day + (first_day_of_month.weekday() + 1)) // 7 + 1 # понадобится при работе с моделями

    start_date = ts.utc(date(year, month, 1))
    transits = await calculate_transits_for_natal_chart(start_date=start_date, end_date=start_date)

    data = generate_horoscope(transits, horoscope_type=2)
    lunar_phase = await get_current_lunar_phase(session, year, month, day)

    return {'lunar phase': lunar_phase, 'data': data} # change return


async def get_horoscope_monthly(session: AsyncSession):
    ts = load.timescale()
    now = datetime.now()
    year, month = now.year, now.month
    start_date = ts.utc(date(year, month, 1))

    transits = await calculate_transits_for_natal_chart(start_date=start_date, end_date=start_date)
    data = generate_horoscope(transits, horoscope_type=3)
    season = get_season(month)

    return {'season': season, 'data': data} # change return


async def get_horoscope_annual(session: AsyncSession):
    ts = load.timescale()
    start_date = ts.utc(date(datetime.now().year, 1, 1))

    transits = await calculate_transits_for_natal_chart(start_date=start_date, end_date=start_date)

    data = generate_horoscope(transits, horoscope_type=4)

    print(data)

    return data
