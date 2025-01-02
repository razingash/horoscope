from skyfield.jpllib import SpiceKernel

from core.config import BASE_DIR

eph = SpiceKernel(BASE_DIR / 'services/de440.bsp')
