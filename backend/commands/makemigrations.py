from alembic import command
from alembic.config import Config
from colorama import Style, Fore


def command_makemigrations(): # improve
    try:
        alembic_cfg = Config("alembic.ini")
        command.revision(alembic_cfg, message=None, autogenerate=True)
    except Exception as e:
        print(e)
    else:
        print(Style.BRIGHT + Fore.GREEN + 'success')

