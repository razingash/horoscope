import argparse
import asyncio
import os
import random

from colorama import init, Fore, Style

from core.database import db_session
from alembic.config import Config
from alembic import command
from core.models import Base

"""Commands for easy interaction with the AioSqlite3 database and initial data"""


async def clear_db(): # later make from it reinitialization command
    if os.path.exists('db.sqlite3'):
        async with db_session.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print(Style.BRIGHT + Fore.GREEN + "Database cleared")
    else:
        print(Fore.RED + "Database doesn't exists")


def deinitialization():
    """delete database, LATER also delete mediafiles? and migrations??"""
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print(Style.BRIGHT + Fore.GREEN + "deinitialization were successful")
    else:
        print(Fore.RED + "Database doesn't exists")


def makemigrations(): # improve
    try:
        alembic_cfg = Config("alembic.ini")
        message = str(random.random())
        command.revision(alembic_cfg, message=message, autogenerate=True)
    except Exception as e:
        print(e)
    else:
        print(Style.BRIGHT + Fore.GREEN + 'success')


def migrate():
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        print(e)
    else:
        print(Style.BRIGHT + Fore.GREEN + 'success')


def main():
    parser = argparse.ArgumentParser(description="Database management commands")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser('clear_db', help='clear database')
    subparsers.add_parser('delete_db', help='remove database')
    subparsers.add_parser('makemigrations', help='make migrations')
    subparsers.add_parser('migrate', help='apply migrations')

    args = parser.parse_args()
    if args.command == 'clear_db':
        asyncio.run(clear_db())
    elif args.command == 'deinitialization':
        deinitialization()
    elif args.command == 'makemigrations':
        makemigrations()
    elif args.command == 'migrate':
        migrate()


if __name__ == "__main__":
    init(autoreset=True)
    main()
