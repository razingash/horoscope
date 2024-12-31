import argparse
import asyncio
import json
import os

from colorama import init, Fore, Style

from alembic.config import Config
from alembic import command
from core.config import BASE_DIR
from core.database import db_session
from core.models import HoroscopePatterns

"""Commands for easy interaction with the AioSqlite3 database and initial data"""

async def generate_static_data():
    print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + 'generating static data')

    fixtures_dir = os.path.join(BASE_DIR, 'fixtures', 'horoscope', 'daily')
    file_names = ['1_aries', '2_taurus', '3_gemini', '4_cancer', '5_leo', '6_virgo', '7_libra', '8_scorpius',
                  '9_saggitarius', '10_capricornus', '11_aquarius', '12_pisces']
    async with db_session.session_factory()as session:
        try:
            for zodiac_index, file_name in enumerate(file_names, 1):
                file_path = os.path.join(fixtures_dir, f"{file_name}.json")
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for language_item in data.get('language', []):
                            for lang_key, lang_data in language_item.items():
                                for house_data in lang_data:
                                    planet = house_data.get('planet')
                                    for house in house_data.get('houses', []):
                                        house_number = house.get('house')
                                        for aspect in house.get('aspects', []):
                                            aspect_type = aspect.get('aspect')
                                            description = aspect.get('description')
                                            hp = HoroscopePatterns(
                                                type='daily', language=lang_key,
                                                planet=planet, house=house_number,
                                                zodiac=zodiac_index, aspect=aspect_type,
                                                description=description
                                            )
                                            session.add(hp)
                await session.commit()
        except Exception as e:
            await session.rollback()
            print(e)
        else:
            print(Style.BRIGHT + Fore.GREEN + 'Static data generation has been completed')


def deinitialization(): # вместо того чтобы удалять миграции сделать чтобы они не создавались если нет изменений
    """delete database and migrations"""
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print(Style.BRIGHT + Fore.GREEN + "deinitialization completed")
    else:
        print(Fore.RED + "Database doesn't exists")


def initialization():
    makemigrations()
    migrate()
    asyncio.run(generate_static_data())

def makemigrations(): # improve
    try:
        alembic_cfg = Config("alembic.ini")
        command.revision(alembic_cfg, message=None, autogenerate=True)
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

    subparsers.add_parser('initialization', help='initialize the database with static data')
    subparsers.add_parser('deinitialization', help='remove database')
    subparsers.add_parser('makemigrations', help='make migrations')
    subparsers.add_parser('migrate', help='apply migrations')

    args = parser.parse_args()
    if args.command == 'initialization':
        initialization()
    elif args.command == 'deinitialization':
        deinitialization()
    elif args.command == 'makemigrations':
        makemigrations()
    elif args.command == 'migrate':
        migrate()


if __name__ == "__main__":
    init(autoreset=True)
    main()
