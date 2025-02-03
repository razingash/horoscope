from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_session
from services.solar_system.services import calculate_helio_angles

router = APIRouter()

@router.get(path='/map/')
async def get_solar_system_map(session: AsyncSession = Depends(db_session.session_dependency)):
    ss_map = calculate_helio_angles()
    return ss_map
