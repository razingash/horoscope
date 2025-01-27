from enum import Enum

__all__ = [
    "LanguagesChoices", "PlanetsChoices", "ZodiacsChoices", "HousesChoices", "AspectsChoices", "MoonEventsChoices",
    "HoroscopeTypes", "MoonPhasesChoices", "EarthSeasons"
]

class LanguagesChoices(str, Enum):
    RUSSIAN = "ru"
    ENGLISH = "en"
    POLISH = "pl"


class HoroscopeTypes(int, Enum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    ANNUAL = 4


class PlanetsChoices(int, Enum):
    SUN = 1
    MERCURY = 2
    VENUS = 3
    MOON = 4
    MARS = 5
    JUPITER = 6
    SATURN = 7
    URANUS = 8
    NEPTUNE = 9
    PLUTO = 10


class ZodiacsChoices(int, Enum):
    ARIES = 1
    TAURUS = 2
    GEMINI = 3
    CANCER = 4
    LEO = 5
    VIRGO = 6
    LIBRA = 7
    SCORPIO = 8
    SAGITTARIUS = 9
    CAPRICORN = 10
    AQUARIUS = 11
    PISCES = 12


class HousesChoices(int, Enum):
    HOUSE1 = 1
    HOUSE2 = 2
    HOUSE3 = 3
    HOUSE4 = 4
    HOUSE5 = 5
    HOUSE6 = 6
    HOUSE7 = 7
    HOUSE8 = 8
    HOUSE9 = 9
    HOUSE10 = 10
    HOUSE11 = 11
    HOUSE12 = 12


class AspectsChoices(int, Enum):
    NONE = 0
    CONJUNCTION = 1
    OPPOSITION = 2
    SQUARE = 3
    TRINE = 4
    SEXTILE = 5


class MoonEventsChoices(int, Enum):
    BLUE_MOON = 1
    MICROMOON = 2
    SUPERMOON = 3
    WOLFMOON = 4


class MoonPhasesChoices(int, Enum):
    NEW_MOON = 1
    WAXING_CRESCENT = 2
    FIRST_QUARTER = 3
    WAXING_GIBBOUS = 4
    FULL_MOON = 5
    WANING_GIBBOUS = 6
    THIRD_QUARTER = 7
    WANING_CRESCENT = 8


class EarthSeasons(int, Enum):
    SPRING = 1
    SUMMER = 2
    AUTUMN = 3
    WINTER = 4
