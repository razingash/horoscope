import os

from colorama import Style, Fore


def command_deinitialization():
    """delete database and migrations"""
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print(Style.BRIGHT + Fore.GREEN + "deinitialization completed")
    else:
        print(Fore.RED + "Database doesn't exists")


