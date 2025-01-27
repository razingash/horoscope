from datetime import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import MoonEventsSchedule, MoonPhases, MoonEvents
from services.moon.services import get_moon_phases

"""
тут как кэшировать пока не уверен
"""
# привести запросы к общему виду(тяжкость бытия)
async def get_moon_phases_with_events(session: AsyncSession, year: int):
    raw_query = text("""
        SELECT 
            strftime('%Y-%m-%d %H:%M:%S', mp.date) AS "datetime",
            mp.phase AS "phase",
            CASE 
                WHEN COUNT(me.event) > 0 THEN json_group_array(me.event)
                ELSE NULL 
            END AS events
        FROM 
            moon_phases mp
        LEFT JOIN 
            moon_events me ON mp.id = me.phase_id
        WHERE 
            strftime('%Y', mp.date) = :year
        GROUP BY 
            mp.id, mp.date, mp.phase
        ORDER BY 
            mp.date;
    """)

    params = {"year": str(year)}
    result = await session.execute(raw_query, params)
    moon_phases = result.mappings().all()

    if not moon_phases:
        moon_phases = get_moon_phases(year=year, start_month=1, end_month=12)

        moon_event_schedule = MoonEventsSchedule(year=year)
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
