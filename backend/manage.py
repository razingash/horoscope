import argparse
import importlib

from colorama import init

"""Commands for easy interaction with the AioSqlite3 database and initial data"""


def main():
    parser = argparse.ArgumentParser(description="Database management commands")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser('initialization', help='initialize the database with static data')
    subparsers.add_parser('deinitialization', help='remove database')
    subparsers.add_parser('makemigrations', help='make migrations')
    subparsers.add_parser('migrate', help='apply migrations')

    postinitialization_pasresr = subparsers.add_parser('postinitialization', help="calculate data for a time period - starting from the day before last, ending with the selected one")
    postinitialization_pasresr.add_argument('end_date', type=str, help="The end date for calculation (format: YYYY-MM-DD)")

    args = parser.parse_args()
    if args.command == 'initialization':
        command = importlib.import_module('commands.initialization')
        command.command_initialization()
    elif args.command == 'deinitialization':
        command = importlib.import_module('commands.deinitialization')
        command.command_deinitialization()
    elif args.command == 'makemigrations':
        command = importlib.import_module('commands.makemigrations')
        command.command_makemigrations()
    elif args.command == 'migrate':
        command = importlib.import_module('commands.migrate')
        command.command_migrate()
    elif args.command == 'postinitialization':
        from colorama import Fore
        from datetime import datetime

        try:
            end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
            if datetime(2650, 1, 25) < end_date < datetime(1549, 12, 31):
                raise PermissionError
            command = importlib.import_module('commands.postinitialization')
            command.command_postinitialization(end_date)
        except ValueError:
            print(Fore.LIGHTRED_EX + "Invalid date format. You need to use YYYY-MM-DD.")
        except PermissionError:
            print(Fore.LIGHTRED_EX + "The date should be between 1549-12-31 and 2650-1-25")


if __name__ == "__main__":
    init(autoreset=True)
    main()
