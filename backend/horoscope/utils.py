from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from services.moon.services import get_moon_phases


def get_season(month: int) -> int:
    if month in [12, 1, 2]:
        return 4 # winter
    elif month in [3, 4, 5]:
        return 1 # spring
    elif month > 9:
        return 3 # autumn
    else:
        return 2 # summer


async def get_current_lunar_phase(session: AsyncSession, year: int, month: int, day: int) -> int:
    """Is this really supposed to be here?"""
    lunar_phases = await get_moon_phases(session, year, month)
    lunar_phases = lunar_phases['moon_phases']
    target_date = datetime(year, month, day)

    for item in lunar_phases:
        item['datetime'] = datetime.strptime(item['datetime'], '%Y-%m-%d %H:%M:%S')

    closest_event = min(lunar_phases, key=lambda x: abs(x['datetime'] - target_date))['phase']

    return closest_event
