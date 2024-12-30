from enum import Enum

__all__ = [
    "LanguagesChoices", "PlanetsChoices", "ZodiacsChoices", "HousesChoices", "AspectsChoices", "MoonEventsChoices",
    "HoroscopeTypes"
]

class LanguagesChoices(str, Enum):
    russian = "ru"
    english = "eng"
    polish = "pl"


class HoroscopeTypes(int, Enum):
    daily = 1
    weekly = 2
    monthly = 3
    annual = 4


class PlanetsChoices(int, Enum):
    sun = 1
    mercury = 2
    venus = 3
    moon = 4
    mars = 5
    jupiter = 6
    saturn = 7
    uranus = 8
    neptune = 9
    pluto = 10


class ZodiacsChoices(int, Enum):
    aries = 1
    taurus = 2
    gemini = 3
    cancer = 4
    leo = 5
    virgo = 6
    libra = 7
    scorpio = 8
    sagittarius = 9
    capricorn = 10
    aquarius = 11
    pisces = 12


class HousesChoices(int, Enum):
    house1 = 1
    house2 = 2
    house3 = 3
    house4 = 4
    house5 = 5
    house6 = 6
    house7 = 7
    house8 = 8
    house9 = 9
    house10 = 10
    house11 = 11
    house12 = 12


class AspectsChoices(int, Enum):
    conjunction = 1
    opposition = 2
    square = 3
    trine = 4
    sextile = 5


class MoonEventsChoices(int, Enum):
    blue_moon = 1
    micromoon = 2
    supermoon = 3
