import pytz

from core.ephemeris import eph


def calculate_transits_for_natal_chart(start_date, end_date):
    """! сейчас временная зона - UTC, это подходит для гороскопа но для натальной фигни нужно будет выбирать временную зону
    """
    planets = { # PlanetsChoices
        1: eph['sun'],
        2: eph['mercury barycenter'],
        3: eph['venus barycenter'],
        4: eph['earth barycenter'],
        5: eph['mars barycenter'],
        6: eph['jupiter barycenter'],
        7: eph['saturn barycenter'],
        8: eph['uranus barycenter'],
        9: eph['neptune barycenter'],
        10: eph['pluto barycenter']
    }
    observer = eph['earth']
    local_transits = {}
    local_tz = pytz.timezone('UTC') # мб получится убрать эту таймзону поскольку там по умолчанию UTC

    for planet_name, target_planet in planets.items():
        times, elongations = [], []
        t = start_date
        while t.tt <= end_date.tt:
            apparent_position = observer.at(t).observe(target_planet)

            sun_position = observer.at(t).observe(eph['sun'])

            elongation = apparent_position.separation_from(sun_position)
            elongations.append(elongation.degrees)
            times.append(t)

            t = t + 1

        local_planet_transits = []
        for time, elongation in zip(times, elongations):
            utc_time_obj = time.utc_datetime()

            if utc_time_obj.tzinfo is None:
                utc_time_obj = pytz.utc.localize(utc_time_obj)

            local_time = utc_time_obj.astimezone(local_tz)
            local_planet_transits.append((local_time, elongation))

        local_transits[planet_name] = local_planet_transits

    return local_transits
