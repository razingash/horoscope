from datetime import datetime

from core.models import EarthSeasons
from services.moon.services import get_moon_phases


def get_season(month: int) -> int:
    if month in [12, 1, 2]:
        return EarthSeasons.WINTER
    elif month in [3, 4, 5]:
        return EarthSeasons.SPRING
    elif month > 9:
        return EarthSeasons.AUTUMN
    else:
        return EarthSeasons.SUMMER


def get_current_lunar_phase(year: int, month: int, day: int) -> int:
    """Is this really supposed to be here?"""
    lunar_phases = get_moon_phases(year, month)

    target_date = datetime(year, month, day)

    for item in lunar_phases:
        item['datetime'] = datetime.strptime(item['datetime'], '%Y-%m-%d %H:%M:%S')

    closest_event = min(lunar_phases, key=lambda x: abs(x['datetime'] - target_date))['phase']

    return closest_event
