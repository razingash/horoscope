import os
import shutil
from glob import glob
from pathlib import Path

from colorama import Style, Fore

from core.config import BASE_DIR


def command_deinitialization():
    """delete database and migrations"""
    if os.path.exists('db.sqlite3'):
        try:
            migrations_dir = os.path.join(BASE_DIR, 'alembic', 'versions')
            os.remove('db.sqlite3')
            migrations = glob(os.path.join(migrations_dir, "*"))
            for migration in migrations:
                if Path(migration).is_file():
                    os.remove(migration)
                elif Path(migration).is_dir():
                    shutil.rmtree(migration)
        except PermissionError:
            print(Fore.LIGHTRED_EX + "the file is occupied by another process, most likely the database is open in some other application")
        else:
            print(Style.BRIGHT + Fore.GREEN + "deinitialization completed")
    else:
        print(Fore.RED + "Database doesn't exists")


