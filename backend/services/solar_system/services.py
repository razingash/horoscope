import math

from skyfield.api import load
from datetime import datetime

from core.config import eph


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
