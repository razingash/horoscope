import os
from pathlib import Path

from skyfield.jpllib import SpiceKernel

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_DIR = os.path.join(BASE_DIR, 'media')

DATABASE = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
ALEMBIC_INI_PATH = f'{BASE_DIR}/alembic.ini'

eph = SpiceKernel(BASE_DIR / 'services/de440.bsp')

