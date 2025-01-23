from datetime import datetime, timedelta

from services.horoscope.prediction import get_week_number, calculate_ascendant


def test_get_week_number():
    res = [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5]
    for day in range(1, 32):
        fp = get_week_number(2025, 1, day)
        res.append(fp)

    res = [2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5]
    for day in range(1, 29):
        fp = get_week_number(2025, 2, day)
        res.append(fp)


def test_calculate_ascendant():
    res = [0.9863013698630136, 1.9726027397260273, 2.958904109589041, 3.9452054794520546, 358.027397260274,
           359.01369863013696, 0.0]
    days = [1, 2, 3, 4, 363, 364, 365]
    for res, day in zip(res, days):
        day_of_year = datetime(2025, 1, 1) + timedelta(days=day - 1)
        ascendant = calculate_ascendant(day_of_year=day_of_year)
        assert ascendant == res, "Results do not match the true ones"
