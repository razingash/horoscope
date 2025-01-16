import argparse

from colorama import init

from commands import command_makemigrations, command_initialization, command_deinitialization, command_migrate

"""Commands for easy interaction with the AioSqlite3 database and initial data"""


def main():
    parser = argparse.ArgumentParser(description="Database management commands")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser('initialization', help='initialize the database with static data')
    subparsers.add_parser('deinitialization', help='remove database')
    subparsers.add_parser('makemigrations', help='make migrations')
    subparsers.add_parser('migrate', help='apply migrations')

    args = parser.parse_args()
    if args.command == 'initialization':
        command_initialization()
    elif args.command == 'deinitialization':
        command_deinitialization()
    elif args.command == 'makemigrations':
        command_makemigrations()
    elif args.command == 'migrate':
        command_migrate()


if __name__ == "__main__":
    init(autoreset=True)
    main()
