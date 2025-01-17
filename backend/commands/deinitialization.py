import os
from glob import glob
from colorama import Style, Fore

from core.config import BASE_DIR


def command_deinitialization():
    """delete database and migrations"""
    if os.path.exists('db.sqlite3'):
        try:
            migrations_dir = os.path.join(BASE_DIR, 'alembic', 'versions')
            os.remove('db.sqlite3')
            migrations = glob(os.path.join(migrations_dir, "*"))
            [os.remove(migration) for migration in migrations]
        except PermissionError:
            print(Fore.LIGHTRED_EX + "the file is occupied by another process, most likely the database is open in some application")
        else:
            print(Style.BRIGHT + Fore.GREEN + "deinitialization completed")
    else:
        print(Fore.RED + "Database doesn't exists")


