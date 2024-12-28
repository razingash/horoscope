from sqlalchemy import select
from sqlalchemy.orm import Session

from core.models import MoonEventsSchedule


async def get_moon_schedule_path(session: Session, date):
    stmt = select(MoonEventsSchedule.path).where(MoonEventsSchedule.date == date)
    result = await session.execute(stmt) # если урбать то будет ошибка
    return result.scalar_one_or_none()

async def add_moon_schedule(session: Session, event_date, path): # for one month
    event = MoonEventsSchedule(date=event_date, path=path)
    session.add(event)
    await session.commit()
    await session.refresh(event)

