from core.models import EarthSeasons

def get_season(month: int) -> int:
    if month in [12, 1, 2]:
        return EarthSeasons.WINTER
    elif month in [3, 4, 5]:
        return EarthSeasons.SPRING
    elif month > 9:
        return EarthSeasons.AUTUMN
    else:
        return EarthSeasons.SUMMER
