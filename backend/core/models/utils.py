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
    Sun = 1
    Mercury = 2
    Venus = 3
    Moon = 4
    Mars = 5
    Jupiter = 6
    Saturn = 7
    Uranus = 8
    Neptune = 9
    Pluto = 10


class ZodiacsChoices(int, Enum):
    Aries = 1
    Taurus = 2
    Gemini = 3
    Cancer = 4
    Leo = 5
    Virgo = 6
    Libra = 7
    Scorpio = 8
    Sagittarius = 9
    Capricorn = 10
    Aquarius = 11
    Pisces = 12


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
    none = 0
    conjunction = 1
    opposition = 2
    square = 3
    trine = 4
    sextile = 5


class MoonEventsChoices(int, Enum):
    blue_moon = 1
    micromoon = 2
    supermoon = 3
