from enum import Enum


class Planets(int, Enum):
    mercury = 1
    venus = 2
    earth = 3
    mars = 4
    jupiter = 5
    saturn = 6
    uranus = 7
    neptune = 8
    pluto = 9
    sun = 10


class Zodiacs(int, Enum):
    oven = 1
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


class Houses(int, Enum):
    first = 1
    second = 2
    third = 3
    fourth = 4
    fifth = 5
    sixth = 6
    seventh = 7
    eighth = 8
    ninth = 9
    tenth = 10
    eleventh = 11
    twelfth = 12
