from datetime import timezone, timedelta, datetime

from skyfield.api import load
from sqlalchemy import select
from calendar import monthrange
from core.database import db_session
from core.models import HoroscopeDaily, HoroscopeWeekly, HoroscopeMonthly, HoroscopeAnnual, HoroscopeTypes, \
    HoroscopeFitDaily, HoroscopeVoidDaily, HoroscopeVoidMonthly, HoroscopeFitMonthly, HoroscopeVoidAnnual, \
    HoroscopeFitAnnual, HoroscopeVoidWeekly, HoroscopeFitWeekly, LanguagesChoices, ZodiacsChoices
from asyncio import run as asyncio_run

from horoscope.utils import get_current_lunar_phase, get_season
from services.horoscope.natal_chart import calculate_transits_for_natal_chart
from services.horoscope.prediction import horoscope_daily, horoscope_weekly, horoscope_monthly, \
    horoscope_annual


def command_postinitialization(end_date):
    """calculates static data starting from the day before yesterday, ending with the selected day"""
    asyncio_run(calculate_horoscope_data(end_date))


async def calculate_horoscope_data(end_date) -> None:
    ts = load.timescale()
    start_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    start_date, end_date = ts.utc(start_date), ts.utc(end_date.replace(tzinfo=timezone.utc))

    data = await generate_future_horoscope(start_date=start_date, end_date=end_date)


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
                first_day_of_month = datetime(year, month, 1)
                week_number_of_month = (day + (first_day_of_month.weekday() + 1)) // 7 + 1

                horoscope_data = await get_weekly_horoscope_descriptions(session, current_date, data)

                await fill_horoscope(model_class=HoroscopeWeekly, data=horoscope_data,
                                     week_number=week_number_of_month, month=month, year=year)

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

""" ! оптимизировать только после того как сделаю тесты для критических функций
async def get_horoscope_descriptions(session, **kwargs):
    descriptions = {language.value: {} for language in LanguagesChoices}
    for language in LanguagesChoices:
        for info in kwargs["data"]:
            zodiac = info['zodiac']
"""

async def get_daily_horoscope_descriptions(session, data):
    moon_position = data["moon_position"]
    moon_cycle = data["moon_cycle"]
    data = data["data"]

    descriptions = {language.value: {} for language in LanguagesChoices}
    for language in LanguagesChoices:
        for info in data:
            zodiac = info['zodiac']
            planet = info.get('planet')

            if planet is None:  # void
                HoroscopeVoidDaily()
                query = select(HoroscopeVoidDaily.description).filter(
                    HoroscopeVoidDaily.zodiac == zodiac,
                    HoroscopeVoidDaily.moon_position == moon_position,
                    HoroscopeVoidDaily.moon_cycle == moon_cycle,
                    HoroscopeVoidDaily.language == language,
                )
            else:  # fit
                aspect = info["aspect"]
                house = info['house']
                query = select(HoroscopeFitDaily.description).filter(
                    HoroscopeFitDaily.aspect == aspect,
                    HoroscopeFitDaily.zodiac == zodiac,
                    HoroscopeFitDaily.house == house,
                    HoroscopeFitDaily.planet == planet,
                    HoroscopeFitDaily.language == language,
                )

            result = await session.execute(query)
            zodiac_description = result.scalars().first()

            if zodiac_description:
                descriptions[language.value][zodiac] = zodiac_description

    return descriptions


async def get_weekly_horoscope_descriptions(session, choosen_date, data):
    year, month, day = choosen_date.year, choosen_date.month, choosen_date.day
    lunar_phase = await get_current_lunar_phase(session, year, month, day)

    descriptions = {language.value: {} for language in LanguagesChoices}
    for language in LanguagesChoices:
        for info in data:
            zodiac = info['zodiac']
            house = info['house']

            planet = info.get('planet')

            if planet is None: # void # lunar_phase
                planet_position = info.get('planet_position')
                query = select(HoroscopeVoidWeekly.description).filter(
                    HoroscopeVoidWeekly.lunar_phase == lunar_phase,
                    HoroscopeVoidWeekly.zodiac == zodiac,
                    HoroscopeVoidWeekly.house == house,
                    HoroscopeVoidWeekly.main_planet_position == planet_position,
                    HoroscopeVoidWeekly.language == language,
                )
            else: # fit # lunar phase
                query = select(HoroscopeFitWeekly.description).filter(
                    HoroscopeFitWeekly.lunar_phase == lunar_phase,
                    HoroscopeFitWeekly.zodiac == zodiac,
                    HoroscopeFitWeekly.house == house,
                    HoroscopeFitWeekly.planet == planet,
                    HoroscopeFitWeekly.language == language,
                )

            result = await session.execute(query)
            zodiac_description = result.scalars().first()

            if zodiac_description:
                descriptions[language.value][zodiac] = zodiac_description

    return descriptions


async def get_monthly_horoscope_descriptions(session, data, season):
    descriptions = {language.value: {} for language in LanguagesChoices}
    for language in LanguagesChoices:
        for info in data:
            zodiac = info['zodiac']
            house = info['house']

            planet = info.get('planet')

            if planet is None:  # void
                planet_position = info.get('planet_position')
                query = select(HoroscopeVoidMonthly.description).filter(
                    HoroscopeVoidMonthly.zodiac == zodiac,
                    HoroscopeVoidMonthly.house == house,
                    HoroscopeVoidMonthly.main_planet_position == planet_position,
                    HoroscopeVoidMonthly.language == language,
                )
            else:  # fit
                query = select(HoroscopeFitMonthly.description).filter(
                    HoroscopeFitMonthly.season == season,
                    HoroscopeFitMonthly.zodiac == zodiac,
                    HoroscopeFitMonthly.house == house,
                    HoroscopeFitMonthly.planet == planet,
                    HoroscopeFitMonthly.language == language,
                )

            result = await session.execute(query)
            zodiac_description = result.scalars().first()

            if zodiac_description:
                descriptions[language.value][zodiac] = zodiac_description

    return descriptions


async def get_annual_horoscope_descriptions(session, data):
    descriptions = {language.value: {} for language in LanguagesChoices}
    for language in LanguagesChoices:
        for info in data:
            zodiac = info['zodiac']
            house = info['house']

            planet = info.get('planet')

            if planet is None:  # void
                planet_position = info.get('planet_position')
                query = select(HoroscopeVoidAnnual.description).filter(
                    HoroscopeVoidAnnual.zodiac == zodiac,
                    HoroscopeVoidAnnual.house == house,
                    HoroscopeVoidAnnual.main_planet_position == planet_position,
                    HoroscopeVoidAnnual.language == language,
                )
            else:  # fit
                query = select(HoroscopeFitAnnual.description).filter(
                    HoroscopeFitAnnual.zodiac == zodiac,
                    HoroscopeFitAnnual.house == house,
                    HoroscopeFitAnnual.planet == planet,
                    HoroscopeFitAnnual.language == language,
                )

            result = await session.execute(query)
            zodiac_description = result.scalars().first()

            if zodiac_description:
                descriptions[language.value][zodiac] = zodiac_description

    return descriptions


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
