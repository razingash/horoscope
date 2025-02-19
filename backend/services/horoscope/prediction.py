from datetime import datetime, timezone

from skyfield.api import load
from sqlalchemy import select

from core.models import PlanetsChoices, LanguagesChoices, HoroscopeVoidAnnual, HoroscopeFitAnnual, HoroscopeVoidMonthly, \
    HoroscopeFitMonthly, HoroscopeFitWeekly, HoroscopeVoidWeekly, HoroscopeFitDaily, HoroscopeVoidDaily
from services.horoscope.natal_chart import calculate_transits_for_natal_chart
from services.moon.services import get_moon_cycle, get_current_lunar_phase


def generate_horoscope(horoscope_type: int, start_date, end_date=None):
    """Generates a horoscope based on transits and aspects between planets"""
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
    ts = load.timescale()
    start_date = ts.utc(start_date)

    if end_date is None:
        end_date = start_date

    transits = calculate_transits_for_natal_chart(start_date=start_date, end_date=end_date)

    if horoscope_type == 1:
        return horoscope_daily(transits, zodiac_planet_association)
    elif horoscope_type == 2:
        return horoscope_weekly(transits, zodiac_planet_association)
    elif horoscope_type == 3:
        return horoscope_monthly(transits, zodiac_planet_association)
    elif horoscope_type == 4:
        return horoscope_annual(transits, zodiac_planet_association)


def horoscope_daily(transits: dict, zodiac_planet_association: list, choosed_time=None) -> dict:
    aspect_definitions = {  # details in AspectsChoices
        1: (0, 8),  # conjunction: 0° ± 8°
        2: (180, 8),  # opposition: 180° ± 8°
        3: (90, 8),  # square: 90° ± 8°
        4: (120, 8),  # trine: 120° ± 8°
        5: (60, 6)  # sextile: 60° ± 6°
    }
    daily_aspects = []

    planet_names = list(transits.keys())
    planet_positions = {planet: transits[planet][0][1] for planet in planet_names}

    planet_names_count = len(planet_names)
    for j in range(planet_names_count):
        for k in range(j + 1, planet_names_count):
            planet1 = planet_names[j]
            planet2 = planet_names[k]
            angle = abs(planet_positions[planet1] - planet_positions[planet2]) % 360
            angle = min(angle, 360 - angle)
            for aspect_name, (ideal_angle, orb) in aspect_definitions.items():
                if abs(angle - ideal_angle) <= orb:
                    daily_aspects.append((planet1, planet2, aspect_name))

    zodiac_planets, planet_house, zodiac_house_shift = interpret_transits(transits)
    matched_zodiac_planets = get_matched_zodiac_planets(zodiac_planets, zodiac_planet_association)

    data = correlate_horoscope_data_daily(
        zodiac_planets=matched_zodiac_planets, planet_house=planet_house, zodiac_house_shift=zodiac_house_shift,
        aspects=daily_aspects, zodiac_planet_association=zodiac_planet_association, choosed_time=choosed_time
    )
    return data


def horoscope_weekly(transits: dict, zodiac_planet_association: list) -> list:
    zodiac_planets, planet_house, zodiac_house_shift = interpret_transits(transits)
    matched_zodiac_planets = get_matched_zodiac_planets(zodiac_planets, zodiac_planet_association)

    data = correlate_horoscope_data_default(
        zodiac_planets=matched_zodiac_planets, planet_house=planet_house,
        zodiac_house_shift=zodiac_house_shift, zodiac_planet_association=zodiac_planet_association
    )
    return data


def horoscope_monthly(transits: dict, zodiac_planet_association: list) -> list:
    zodiac_planets, planet_house, zodiac_house_shift = interpret_transits(transits)
    matched_zodiac_planets = get_matched_zodiac_planets(zodiac_planets, zodiac_planet_association)

    data = correlate_horoscope_data_default(
        zodiac_planets=matched_zodiac_planets, planet_house=planet_house,
        zodiac_house_shift=zodiac_house_shift, zodiac_planet_association=zodiac_planet_association
    )
    return data


def horoscope_annual(transits: dict, zodiac_planet_association: list) -> list:
    zodiac_planets, planet_house, zodiac_house_shift = interpret_transits(transits)
    matched_zodiac_planets = get_matched_zodiac_planets(zodiac_planets, zodiac_planet_association)

    correlated_data = correlate_horoscope_data_default(
        zodiac_planets=matched_zodiac_planets, planet_house=planet_house,
        zodiac_house_shift=zodiac_house_shift, zodiac_planet_association=zodiac_planet_association
    )
    return correlated_data


def correlate_horoscope_data_default(
        zodiac_planets: dict, planet_house: dict, zodiac_house_shift: int, zodiac_planet_association: list
) -> list:
    """Annual, Monthly and weekly horoscopes.\n
    correlates the positions of planets in the field of the zodiac sign or the main planet of the sign, if the sign is empty
    """

    new_data = []
    for i in range(1, 13):
        zodiac_planet = zodiac_planets.get(i)
        house = (i + zodiac_house_shift - 1) % 12 + 1
        if zodiac_planet:
            pattern = {
                "zodiac": i,
                "house": house,
                "planet": zodiac_planet,
            }
        else:
            primary_planet_for_sign = zodiac_planet_association[i - 1][0]
            house_position = planet_house.get(primary_planet_for_sign, None)

            pattern = {
                "zodiac": i,
                "house": house,
                "planet_position": house_position,  # Primary planet position of the sign
            }

        new_data.append(pattern)

    return new_data


def correlate_horoscope_data_daily( # возможно лучше будет даже не добавлять данные с пустыми зодиаками
        zodiac_planets: dict, planet_house: dict,  aspects: list, zodiac_planet_association: list,
        zodiac_house_shift: int, choosed_time=None
) -> dict:
    """ Daily horoscope\n
    selects more suitable planets and aspects for a particular zodiac sign, if necessary"""
    moon_position = (planet_house[PlanetsChoices.MOON] - zodiac_house_shift - 1) % 12 + 1

    if choosed_time is None:
        choosed_time = datetime.now(timezone.utc)
    moon_cycle = get_moon_cycle(choosed_time)

    new_data = {
        "moon_cycle": moon_cycle, # one of 30
        "moon_position": moon_position,
        "data": []
    }
    for i in range(1, 13):
        zodiac_planet = zodiac_planets.get(i)

        house = (i + zodiac_house_shift - 1) % 12 + 1
        if zodiac_planet:
            planet_aspects = [aspect for aspect in aspects if zodiac_planet in aspect[:2]]

            if planet_aspects:
                prioritized_aspects = sorted(
                    planet_aspects,
                    key=lambda aspect: zodiac_planet_association[i].index(
                        aspect[1] if aspect[0] == zodiac_planet else aspect[0])
                    if (aspect[1] if aspect[0] == zodiac_planet else aspect[0]) in zodiac_planet_association[i]
                    else len(zodiac_planet_association[i])
                )
                aspect = prioritized_aspects[0][2]
            else:
                aspect = 0

            pattern = {
                "zodiac": i,
                "house": house,
                "planet": zodiac_planet,
                "aspect": aspect
            }
        else:
            pattern = {
                "zodiac": i,
            }

        new_data.get("data").append(pattern)
    return new_data


def calculate_house_shift():
    ascendant = calculate_ascendant()
    shift = ascendant % 360
    return int(shift // 30)


def calculate_ascendant(base_ascendant=0, location_offset=0, day_of_year=None): # defaul function for calculating ascendant
    """можно также добавить функцию для рассчета сцендента если нечего делать будет"""
    if day_of_year is None:
        day_of_year = datetime.today()

    day_of_year = day_of_year.timetuple().tm_yday
    ascendant_change_per_day = 360 / 365

    ascendant_position = base_ascendant + (ascendant_change_per_day * day_of_year) + location_offset
    ascendant_position %= 360

    return ascendant_position


def get_zodiac_sign_and_house(elongation): #! Настроить location_offset в самом конце (или же сделать новую функцию)
    sign_index = int(elongation // 30) # same as in ZodiacsChoices + 1
    ascendant = calculate_ascendant(location_offset=0)

    house_position = (elongation - ascendant) % 360 # угол относительно асцендента
    house = int(house_position // 30) + 1 # same as in HousesChoices

    return sign_index, house


def interpret_transits(transits: dict):
    """receives the necessary astronomical data based on transits"""

    planet_names = list(transits.keys())
    planet_positions = {planet: transits[planet][0][1] for planet in planet_names}
    zodiac_planets, planet_house = {}, {}
    zodiac_house_shift = calculate_house_shift()

    for planet, position in planet_positions.items():
        sign, house = get_zodiac_sign_and_house(position)
        if sign not in zodiac_planets:
            zodiac_planets[sign] = []

        zodiac_planets[sign].append(planet)
        planet_house[planet] = house

    return zodiac_planets, planet_house, zodiac_house_shift


def get_matched_zodiac_planets(zodiac_planets: dict, zodiac_planet_association: list) -> dict:
    """arranges more suitable planets for zodiacs"""

    new_zodiac_planets = {}
    for sign, planets in zodiac_planets.items():
        sign += 1
        prioritized_planets = sorted(
            planets,
            key=lambda planet: zodiac_planet_association[sign].index(planet)
            if planet in zodiac_planet_association[sign] else len(zodiac_planet_association[sign])
        )

        primary_planet = prioritized_planets[0]
        new_zodiac_planets[sign] = primary_planet

    return new_zodiac_planets


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
    lunar_phase = get_current_lunar_phase(year, month, day)

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


def get_week_number(year: int, month: int, day: int) -> int:
    """returns the week number of the month"""
    first_day_of_month = datetime(year, month, 1)
    week_number = (day + (first_day_of_month.weekday() + 1)) // 7 + 1

    return week_number
