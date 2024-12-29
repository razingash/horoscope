import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_DIR = os.path.join(BASE_DIR, 'media')

DATABASE = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
