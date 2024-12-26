
from .models.base import Base
from .config import engine

async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def delete_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

