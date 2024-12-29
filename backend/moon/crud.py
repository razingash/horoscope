from sqlalchemy import select
from sqlalchemy.orm import Session

from core.models import MoonEventsSchedule


async def get_moon_schedule_path(session: Session, year: int, month: int):
    stmt = select(MoonEventsSchedule.path).where(
        MoonEventsSchedule.year == year, MoonEventsSchedule.month == month
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def add_moon_schedule(session: Session, year: int, month: int, path: str): # for one month
    event = MoonEventsSchedule(year=year, month=month, path=path)
    session.add(event)
    await session.commit()
    await session.refresh(event)

