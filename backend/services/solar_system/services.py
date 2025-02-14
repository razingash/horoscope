import math

from skyfield.api import load
from datetime import datetime, timedelta, timezone
from json import dumps as json_dumps

from core.ephemeris import eph
from core.database import db_session
from core.models.solar_system import SolarSystemMap


def calculate_helio_angles(date: datetime = datetime.today()) -> dict:
    """calculates the heliocentric angle for the selected date"""

    planets = { # PlanetsChoices
        1: eph['sun'],
        2: eph['mercury barycenter'],
        3: eph['venus barycenter'],
        4: eph['earth barycenter'],
        5: eph['mars barycenter'],
        6: eph['jupiter barycenter'],
        7: eph['saturn barycenter'],
        8: eph['uranus barycenter'],
        9: eph['neptune barycenter'],
        10: eph['pluto barycenter']
    }

    ts = load.timescale()
    t = ts.utc(date.year, date.month, date.day)

    sun_pos = eph['sun'].at(t).position.km

    angles = {}
    for name, planet in planets.items():
        if name > 1:
            planet_pos = planet.at(t).position.km - sun_pos
            x, y = planet_pos[0], planet_pos[1]
            angle = math.degrees(math.atan2(y, x))
            angle = round(angle % 360)
            angles[name] = angle

    return angles


async def generate_solar_system_data(end_date) -> None:
    start_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    current_date = start_date

    data = {}
    i = 0
    array_days = 40
    async with db_session.session_factory() as session:
        batch_counter = 0

        async def commit_if_batch_full():
            nonlocal batch_counter
            if batch_counter >= 1000:
                await session.commit()
                batch_counter = 0

        while current_date <= end_date and i != array_days:
            i += 1
            helio_angles = calculate_helio_angles(current_date)
            data[current_date.strftime("%Y-%m-%d")] = helio_angles

            last_date = current_date
            current_date += timedelta(days=1)
            if i == array_days:
                i = 0
                ss_map = SolarSystemMap(text_data=json_dumps(data), last_date=last_date.date())
                data = {}
                session.add(ss_map)
                batch_counter += 40
                await commit_if_batch_full()
                if current_date >= end_date:
                    break

        await session.commit()
