import json
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, func

from core.models import SolarSystemMap
from services.solar_system.services import generate_solar_system_data

async def get_actual_ss_map(session, nearest_date):
    query = await session.execute(
        select(SolarSystemMap.text_data).order_by(func.abs(SolarSystemMap.last_date - nearest_date.date()))
    )

    result = query.fetchall()

    if result:
        result = json.loads(result[0][0])

    return result


async def get_the_most_suitable_ss_map(session):
    nearest_date = datetime.now(tz=timezone.utc)
    result = await get_actual_ss_map(session, nearest_date)

    if not result: # generate several iterations forward
        end_date = nearest_date + timedelta(days=80)
        await generate_solar_system_data(end_date)

        result = await get_actual_ss_map(session, nearest_date)

    return result
