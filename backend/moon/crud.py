from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import MoonEventsSchedule, MoonPhases, MoonEvents
from services.moon.services import get_moon_phases

"""
тут как кэшировать пока не уверен
"""

async def get_moon_phases_with_events(session: AsyncSession, year: int, month: int):
    # найти нормальный способ убрать лишние поля из этого запроса
    query = await session.execute(select(MoonPhases).join(MoonEventsSchedule).filter(
        MoonEventsSchedule.year == year, MoonEventsSchedule.month == month
    ).options(selectinload(MoonPhases.events)))

    moon_phases = query.unique().scalars().all()

    if not moon_phases:
        moon_phases = get_moon_phases(year=year, month=month)

        moon_event_schedule = MoonEventsSchedule(year=year, month=month)
        session.add(moon_event_schedule)
        await session.flush()
        for mp in moon_phases:
            date = mp["datetime"]
            phase = mp["phase"]
            events = mp.get('events')

            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

            moon_phase = MoonPhases(phase=phase, date=date, schedule_id=moon_event_schedule.id)
            session.add(moon_phase)
            if events is not None:
                await session.flush()
                for event in events:
                    moon_event = MoonEvents(event=event, phase=moon_phase, phase_id=moon_phase.id)
                    session.add(moon_event)

        await session.commit()

    return moon_phases
