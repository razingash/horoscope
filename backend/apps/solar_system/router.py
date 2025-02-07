from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.solar_system.crud import get_the_most_suitable_ss_map
from core.database import db_session

router = APIRouter()

@router.get(path='/map/')
async def get_solar_system_map(session: AsyncSession = Depends(db_session.session_dependency)):
    ss_map = await get_the_most_suitable_ss_map(session)

    return ss_map
