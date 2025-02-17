import os

from colorama import Fore, Style
from skyfield.iokit import Loader
from skyfield.jpllib import SpiceKernel

from core.config import BASE_DIR

def get_ephemeris():
    try:
        eph = SpiceKernel(BASE_DIR / 'services/de440.bsp')
    except FileNotFoundError:
        """checks the presence of a critically important BSP file"""

        directory_path = os.path.join(BASE_DIR, 'services')
        file_path = os.path.join(directory_path, 'de440.bsp')

        if not os.path.exists(file_path):
            print(Fore.LIGHTYELLOW_EX + ".BSP file does not exist, and will be downloaded")

            try:
                custom_loader = Loader(directory=directory_path)
                custom_loader('de440.bsp')

                print(Fore.GREEN + "File 'de440.bsp' successfully downloaded.")

            except Exception as e:
                print(Style.BRIGHT + Fore.RED + "Something went wrong while downloading the file 'de440.bsp'")
                print(e)
            else:
                return SpiceKernel(BASE_DIR / 'services/de440.bsp')
        else:
            print(Fore.GREEN + f"File 'de440.bsp' already exists at {file_path}")
    else:
        return eph

eph = get_ephemeris()
