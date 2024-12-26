import os
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_DIR = os.path.join(BASE_DIR, 'media')

engine = create_async_engine(f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3")

new_session = async_sessionmaker(engine, expire_on_commit=False)
