from sqlalchemy import select

from core.models import MoonEventsSchedule


async def get_moon_events_schedule(date):
    schedule = select(MoonEventsSchedule, )
    return schedule

