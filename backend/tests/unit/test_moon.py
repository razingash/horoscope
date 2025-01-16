import pytz
from datetime import datetime

from skyfield.almanac import moon_phases
from skyfield.api import load
from skyfield.searchlib import find_discrete

from core.constants import eph
from core.models import MoonPhasesChoices
from services.moon.services import find_moon_phases, find_blue_moons, find_supermoons_and_micromoons


def test_find_moon_phases():
    expected_phases = [
        (datetime(2025, 1, 6, 23, 56, 18, tzinfo=pytz.utc), MoonPhasesChoices.FIRST_QUARTER),
        (datetime(2025, 1, 13, 22, 26, 55, tzinfo=pytz.utc), MoonPhasesChoices.FULL_MOON),
        (datetime(2025, 1, 21, 20, 30, 47, tzinfo=pytz.utc), MoonPhasesChoices.THIRD_QUARTER),
        (datetime(2025, 1, 29, 12, 35, 59, tzinfo=pytz.utc), MoonPhasesChoices.NEW_MOON),
        (datetime(2025, 2, 5, 8, 2, 9, tzinfo=pytz.utc), MoonPhasesChoices.FIRST_QUARTER),
        (datetime(2025, 2, 12, 13, 53, 24, tzinfo=pytz.utc), MoonPhasesChoices.FULL_MOON),
        (datetime(2025, 2, 20, 17, 32, 33, tzinfo=pytz.utc), MoonPhasesChoices.THIRD_QUARTER),
        (datetime(2025, 2, 28, 0, 44, 50, tzinfo=pytz.utc), MoonPhasesChoices.NEW_MOON),
        (datetime(2025, 3, 6, 16, 31, 38, tzinfo=pytz.utc), MoonPhasesChoices.FIRST_QUARTER),
        (datetime(2025, 3, 14, 6, 54, 39, tzinfo=pytz.utc), MoonPhasesChoices.FULL_MOON),
        (datetime(2025, 3, 22, 11, 29, 26, tzinfo=pytz.utc), MoonPhasesChoices.THIRD_QUARTER),
        (datetime(2025, 3, 29, 10, 57, 50, tzinfo=pytz.utc), MoonPhasesChoices.NEW_MOON),
        (datetime(2025, 4, 5, 2, 14, 41, tzinfo=pytz.utc), MoonPhasesChoices.FIRST_QUARTER),
        (datetime(2025, 4, 13, 0, 22, 16, tzinfo=pytz.utc), MoonPhasesChoices.FULL_MOON),
        (datetime(2025, 4, 21, 1, 35, 34, tzinfo=pytz.utc), MoonPhasesChoices.THIRD_QUARTER),
        (datetime(2025, 4, 27, 19, 31, 9, tzinfo=pytz.utc), MoonPhasesChoices.NEW_MOON),
        (datetime(2025, 5, 4, 13, 51, 46, tzinfo=pytz.utc), MoonPhasesChoices.FIRST_QUARTER),
        (datetime(2025, 5, 12, 16, 55, 56, tzinfo=pytz.utc), MoonPhasesChoices.FULL_MOON),
        (datetime(2025, 5, 20, 11, 58, 46, tzinfo=pytz.utc), MoonPhasesChoices.THIRD_QUARTER),
        (datetime(2025, 5, 27, 3, 2, 21, tzinfo=pytz.utc), MoonPhasesChoices.NEW_MOON),
        (datetime(2025, 6, 3, 3, 40, 58, tzinfo=pytz.utc), MoonPhasesChoices.FIRST_QUARTER),
        (datetime(2025, 6, 11, 7, 43, 50, tzinfo=pytz.utc), MoonPhasesChoices.FULL_MOON),
        (datetime(2025, 6, 18, 19, 19, 7, tzinfo=pytz.utc), MoonPhasesChoices.THIRD_QUARTER),
        (datetime(2025, 6, 25, 10, 31, 37, tzinfo=pytz.utc), MoonPhasesChoices.NEW_MOON),
        (datetime(2025, 7, 2, 19, 30, 11, tzinfo=pytz.utc), MoonPhasesChoices.FIRST_QUARTER),
        (datetime(2025, 7, 10, 20, 36, 48, tzinfo=pytz.utc), MoonPhasesChoices.FULL_MOON),
        (datetime(2025, 7, 18, 0, 37, 40, tzinfo=pytz.utc), MoonPhasesChoices.THIRD_QUARTER),
        (datetime(2025, 7, 24, 19, 11, 12, tzinfo=pytz.utc), MoonPhasesChoices.NEW_MOON),
        (datetime(2025, 8, 1, 12, 41, 19, tzinfo=pytz.utc), MoonPhasesChoices.FIRST_QUARTER),
        (datetime(2025, 8, 9, 7, 55, 4, tzinfo=pytz.utc), MoonPhasesChoices.FULL_MOON),
        (datetime(2025, 8, 16, 5, 12, 14, tzinfo=pytz.utc), MoonPhasesChoices.THIRD_QUARTER),
        (datetime(2025, 8, 23, 6, 6, 33, tzinfo=pytz.utc), MoonPhasesChoices.NEW_MOON),
        (datetime(2025, 8, 31, 6, 25, 12, tzinfo=pytz.utc), MoonPhasesChoices.FIRST_QUARTER),
        (datetime(2025, 9, 7, 18, 8, 54, tzinfo=pytz.utc), MoonPhasesChoices.FULL_MOON),
        (datetime(2025, 9, 14, 10, 32, 57, tzinfo=pytz.utc), MoonPhasesChoices.THIRD_QUARTER),
        (datetime(2025, 9, 21, 19, 54, 8, tzinfo=pytz.utc), MoonPhasesChoices.NEW_MOON),
        (datetime(2025, 9, 29, 23, 53, 50, tzinfo=pytz.utc), MoonPhasesChoices.FIRST_QUARTER),
        (datetime(2025, 10, 7, 3, 47, 37, tzinfo=pytz.utc), MoonPhasesChoices.FULL_MOON),
        (datetime(2025, 10, 13, 18, 12, 42, tzinfo=pytz.utc), MoonPhasesChoices.THIRD_QUARTER),
        (datetime(2025, 10, 21, 12, 25, 10, tzinfo=pytz.utc), MoonPhasesChoices.NEW_MOON),
        (datetime(2025, 10, 29, 16, 20, 49, tzinfo=pytz.utc), MoonPhasesChoices.FIRST_QUARTER),
        (datetime(2025, 11, 5, 13, 19, 18, tzinfo=pytz.utc), MoonPhasesChoices.FULL_MOON),
        (datetime(2025, 11, 12, 5, 28, 9, tzinfo=pytz.utc), MoonPhasesChoices.THIRD_QUARTER),
        (datetime(2025, 11, 20, 6, 47, 16, tzinfo=pytz.utc), MoonPhasesChoices.NEW_MOON),
        (datetime(2025, 11, 28, 6, 58, 48, tzinfo=pytz.utc), MoonPhasesChoices.FIRST_QUARTER),
        (datetime(2025, 12, 4, 23, 14, 4, tzinfo=pytz.utc), MoonPhasesChoices.FULL_MOON),
        (datetime(2025, 12, 11, 20, 51, 41, tzinfo=pytz.utc), MoonPhasesChoices.THIRD_QUARTER),
        (datetime(2025, 12, 20, 1, 43, 21, tzinfo=pytz.utc), MoonPhasesChoices.NEW_MOON),
        (datetime(2025, 12, 27, 19, 9, 51, tzinfo=pytz.utc), MoonPhasesChoices.FIRST_QUARTER)
    ]

    phases = moon_phases(eph)
    ts = load.timescale()
    times, phase_names = find_discrete(ts.utc(2025, 1, 1), ts.utc(2025, 12, 31), phases)

    result = find_moon_phases(times, phase_names)

    assert len(result) == len(expected_phases), "the number of lunar phases doesn't coincide with the true one"

    for res, exp in zip(result, expected_phases):
        assert res[0] == exp[0], f"Время не совпадает: {res[0]} != {exp[0]}"
        assert res[1] == exp[1], f"Фаза не совпадает: {res[1]} != {exp[1]}"


def test_find_blue_moons():
    expected_moons = [
        datetime(2020, 10, 31, 14, 49, 9, tzinfo=pytz.utc),
        datetime(2023, 8, 31, 1, 35, 38, tzinfo=pytz.utc),
        datetime(2026, 5, 31, 8, 45, 12, tzinfo=pytz.utc),
        datetime(2028, 12, 31, 16, 48, 32, tzinfo=pytz.utc)
    ]

    ts = load.timescale()
    times, phase_names = find_discrete(ts.utc(2020, 1, 1), ts.utc(2030, 12, 31), moon_phases(eph))
    phases = find_moon_phases(times, phase_names)

    result = find_blue_moons(phases)

    assert len(result) == len(expected_moons), "the number of blue moons phases doesn't coincide with the true one"

    for res, exp in zip(result, expected_moons):
        assert res == exp, f"Время не совпадает: {res} != {exp}"


def test_find_supermoons_and_micromoons():
    expected_supermoons = [
        datetime(2020, 3, 9, 17, 47, 45, tzinfo=pytz.utc),
        datetime(2020, 4, 8, 2, 35, 5, tzinfo=pytz.utc),
        datetime(2020, 5, 7, 10, 45, 13, tzinfo=pytz.utc),
        datetime(2021, 4, 27, 3, 31, 33, tzinfo=pytz.utc),
        datetime(2021, 5, 26, 11, 13, 53, tzinfo=pytz.utc),
        datetime(2021, 6, 24, 18, 39, 42, tzinfo=pytz.utc),
        datetime(2022, 6, 14, 11, 51, 46, tzinfo=pytz.utc),
        datetime(2022, 7, 13, 18, 37, 38, tzinfo=pytz.utc),
        datetime(2022, 8, 12, 1, 35, 45, tzinfo=pytz.utc),
        datetime(2023, 8, 1, 18, 31, 40, tzinfo=pytz.utc),
        datetime(2023, 8, 31, 1, 35, 38, tzinfo=pytz.utc),
        datetime(2023, 9, 29, 9, 57, 33, tzinfo=pytz.utc),
        datetime(2024, 9, 18, 2, 34, 28, tzinfo=pytz.utc),
        datetime(2024, 10, 17, 11, 26, 24, tzinfo=pytz.utc),
        datetime(2025, 10, 7, 3, 47, 37, tzinfo=pytz.utc),
        datetime(2025, 11, 5, 13, 19, 18, tzinfo=pytz.utc),
        datetime(2025, 12, 4, 23, 14, 4, tzinfo=pytz.utc),
        datetime(2026, 11, 24, 14, 53, 34, tzinfo=pytz.utc),
        datetime(2026, 12, 24, 1, 28, 14, tzinfo=pytz.utc),
        datetime(2027, 1, 22, 12, 17, 23, tzinfo=pytz.utc),
        datetime(2028, 1, 12, 4, 3, 5, tzinfo=pytz.utc),
        datetime(2028, 2, 10, 15, 3, 46, tzinfo=pytz.utc),
        datetime(2028, 3, 11, 1, 6, 5, tzinfo=pytz.utc),
        datetime(2029, 2, 28, 17, 10, 16, tzinfo=pytz.utc),
        datetime(2029, 3, 30, 2, 26, 25, tzinfo=pytz.utc),
        datetime(2029, 4, 28, 10, 36, 49, tzinfo=pytz.utc),
        datetime(2030, 4, 18, 3, 20, 2, tzinfo=pytz.utc),
        datetime(2030, 5, 17, 11, 19, 10, tzinfo=pytz.utc),
        datetime(2030, 6, 15, 18, 41, 1, tzinfo=pytz.utc),
    ]
    expected_micromoons = [
        datetime(2020, 10, 31, 14, 49, 9, tzinfo=pytz.utc),
        datetime(2021, 12, 19, 4, 35, 31, tzinfo=pytz.utc),
        datetime(2023, 1, 6, 23, 7, 54, tzinfo=pytz.utc),
        datetime(2023, 2, 5, 18, 28, 34, tzinfo=pytz.utc),
        datetime(2024, 2, 24, 12, 30, 26, tzinfo=pytz.utc),
        datetime(2025, 4, 13, 0, 22, 16, tzinfo=pytz.utc),
        datetime(2026, 5, 31, 8, 45, 12, tzinfo=pytz.utc),
        datetime(2027, 7, 18, 15, 44, 56, tzinfo=pytz.utc),
        datetime(2028, 9, 3, 23, 47, 36, tzinfo=pytz.utc),
        datetime(2029, 10, 22, 9, 27, 35, tzinfo=pytz.utc),
        datetime(2030, 12, 9, 22, 40, 28, tzinfo=pytz.utc),
    ]

    ts = load.timescale()
    times, phase_names = find_discrete(ts.utc(2020, 1, 1), ts.utc(2030, 12, 31), moon_phases(eph))
    phases = find_moon_phases(times, phase_names)

    supermoons, micromoons = find_supermoons_and_micromoons(phases)

    assert len(supermoons) == len(expected_supermoons), "the number of blue moons phases doesn't coincide with the true one"
    assert len(micromoons) == len(expected_micromoons), "the number of blue moons phases doesn't coincide with the true one"

    for res, exp in zip(supermoons, expected_supermoons):
        assert res[0] == exp, f"Время не совпадает: {res[0]} != {exp}"

    for res, exp in zip(micromoons, expected_micromoons):
        assert res[0] == exp, f"Время не совпадает: {res[0]} != {exp}"
