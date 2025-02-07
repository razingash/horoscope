from datetime import timezone, timedelta, datetime

from skyfield.api import load
from sqlalchemy import select
from calendar import monthrange
from core.database import db_session
from core.models import HoroscopeDaily, HoroscopeWeekly, HoroscopeMonthly, HoroscopeAnnual, HoroscopeTypes, \
     LanguagesChoices, ZodiacsChoices
from asyncio import run as asyncio_run

from apps.horoscope.utils import get_season
from services.horoscope.natal_chart import calculate_transits_for_natal_chart
from services.horoscope.prediction import horoscope_daily, horoscope_weekly, horoscope_monthly, \
    horoscope_annual, get_week_number, get_annual_horoscope_descriptions, get_monthly_horoscope_descriptions, \
    get_weekly_horoscope_descriptions, get_daily_horoscope_descriptions
from services.solar_system.services import generate_solar_system_data


def command_postinitialization(end_date):
    """calculates static data starting from the day before yesterday, ending with the selected day"""
    asyncio_run(calculate_horoscope_data(end_date))


async def calculate_horoscope_data(end_date) -> None:
    ts = load.timescale()
    start_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    start_date, end_date = ts.utc(start_date), ts.utc(end_date.replace(tzinfo=timezone.utc))

    await generate_solar_system_data(end_date=end_date)
    await generate_future_horoscope(start_date=start_date, end_date=end_date)


async def generate_future_horoscope(start_date, end_date) -> bool:
    """Generates a horoscope based on transits and aspects between planets, over multiple time periods"""
    zodiac_planet_association = [
        [5, 1, 6, 10], # Aries ['Mars', 'Sun', 'Jupiter', 'Pluto']
        [3, 4, 7, 2],  # Taurus ['Venus', 'Moon', 'Saturn', 'Mercury']
        [2, 3, 8, 6],  # Gemini ['Mercury', 'Venus', 'Uranus', 'Jupiter']
        [4, 6, 9, 3],  # Cancer ['Moon', 'Jupiter', 'Neptune', 'Venus']
        [1, 6, 5, 2],  # Leo ['Sun', 'Jupiter', 'Mars', 'Mercury']
        [2, 7, 3],     # Virgo ['Mercury', 'Saturn', 'Venus']
        [3, 7, 2, 4],  # Libra ['Venus', 'Saturn', 'Mercury', 'Moon']
        [10, 5, 4, 9], # Scorpio ['Pluto', 'Mars', 'Moon', 'Neptune']
        [6, 1, 9, 5],  # Sagittarius ['Jupiter', 'Sun', 'Neptune', 'Mars']
        [7, 5, 3, 2],  # Capricorn ['Saturn', 'Mars', 'Venus', 'Mercury']
        [8, 7, 2, 3],  # Aquarius ['Uranus', 'Saturn', 'Mercury', 'Venus']
        [9, 6, 3, 4]   # Pisces ['Neptune', 'Jupiter', 'Venus', 'Moon']
    ]

    try:
        async with db_session.session_factory() as session:
            batch_counter = 0

            async def commit_if_batch_full():
                nonlocal batch_counter
                if batch_counter >= 1000:
                    await session.commit()
                    batch_counter = 0

            async def fill_horoscope(model_class, data, **kwargs):
                nonlocal batch_counter
                for language in LanguagesChoices:
                    language = language.value
                    for zodiac in ZodiacsChoices:
                        zodiac = zodiac.value
                        description = data[language][zodiac]

                        filters = dict(language=language, zodiac=zodiac, **kwargs)
                        existing = await session.execute(select(model_class).filter_by(**filters))

                        if existing.scalar() is None:
                            horoscope = model_class(description=description, **filters)
                            session.add(horoscope)
                            batch_counter += 1

                        await commit_if_batch_full()

            # daily
            for current_date, next_date in daterange(start_date, end_date, HoroscopeTypes.DAILY):
                transits = calculate_transits_for_natal_chart(start_date=current_date, end_date=next_date)

                data = horoscope_daily(transits, zodiac_planet_association)

                current_date = current_date.utc_datetime()
                year, month, day = current_date.year, current_date.month, current_date.day

                horoscope_data = await get_daily_horoscope_descriptions(session, data)

                await fill_horoscope(model_class=HoroscopeDaily, data=horoscope_data, day=day, month=month, year=year)

                await commit_if_batch_full()

            # weekly
            for current_date, next_date in daterange(start_date, end_date, HoroscopeTypes.WEEKLY):
                transits = calculate_transits_for_natal_chart(start_date=current_date, end_date=next_date)
                data = horoscope_weekly(transits, zodiac_planet_association)

                current_date = current_date.utc_datetime()
                year, month, day = current_date.year, current_date.month, current_date.day

                week_number = get_week_number(year, month, day)

                horoscope_data = await get_weekly_horoscope_descriptions(session, current_date, data)

                await fill_horoscope(model_class=HoroscopeWeekly, data=horoscope_data,
                                     week_number=week_number, month=month, year=year)

                await commit_if_batch_full()

            # monthly
            for current_date, next_date in daterange(start_date, end_date, HoroscopeTypes.MONTHLY):
                transits = calculate_transits_for_natal_chart(start_date=current_date, end_date=next_date)
                data = horoscope_monthly(transits, zodiac_planet_association)

                current_date = current_date.utc_datetime()
                year, month = current_date.year, current_date.month
                season = get_season(month)

                horoscope_data = await get_monthly_horoscope_descriptions(session, data, season)

                await fill_horoscope(model_class=HoroscopeMonthly, data=horoscope_data, month=month, year=year)

                await commit_if_batch_full()

            # annual
            for current_date, next_date in daterange(start_date, end_date, HoroscopeTypes.ANNUAL):
                transits = calculate_transits_for_natal_chart(start_date=current_date, end_date=next_date)
                data = horoscope_annual(transits, zodiac_planet_association)

                current_date = current_date.utc_datetime()
                year = current_date.year

                horoscope_data = await get_annual_horoscope_descriptions(session, data)

                await fill_horoscope(model_class=HoroscopeAnnual, data=horoscope_data, year=year)

                await commit_if_batch_full()

            await session.commit()
    except ValueError as e:
        print(e)
        return False
    else:
        return True


"""? ниже сомнительная часть | позже написать тесты для add_month/years"""

def daterange(start_date, end_date, step_type: int):
    current_date = start_date
    while current_date < end_date:
        if step_type == HoroscopeTypes.DAILY:
            next_date = current_date + timedelta(days=1)
        elif step_type == HoroscopeTypes.WEEKLY:
            next_date = current_date + timedelta(weeks=1)
        elif step_type == HoroscopeTypes.MONTHLY:
            next_date = current_date + add_month(start_date)
        elif step_type == HoroscopeTypes.ANNUAL:
            next_date = current_date + add_years(start_date)

        yield current_date, next_date
        current_date = next_date


def add_month(time_obj):
    current_date = time_obj.utc_datetime()
    current_month = current_date.month
    current_year = current_date.year
    day = current_date.day

    if current_month == 12:
        new_year = current_year + 1
        new_month = 1
    else:
        new_year = current_year
        new_month = current_month + 1

    last_day_of_new_month = monthrange(new_year, new_month)[1]
    new_day = min(day, last_day_of_new_month)

    new_date = current_date.replace(year=new_year, month=new_month, day=new_day)

    delta_days = (new_date - current_date).days
    return timedelta(days=delta_days)


def add_years(time_obj):
    current_date = time_obj.utc_datetime()
    new_year = current_date.year + 1

    try:
        new_date = current_date.replace(year=new_year)
    except ValueError:
        new_date = current_date.replace(year=new_year, month=2, day=28)

    delta_days = (new_date - current_date).days
    return timedelta(days=delta_days)
