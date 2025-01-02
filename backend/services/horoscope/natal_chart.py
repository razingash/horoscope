import pytz

from core.constants import eph


def calculate_transits_for_natal_chart(start_date, end_date):
    planets = {
        'sun': eph['sun'],
        'mercury': eph['mercury barycenter'],
        'venus': eph['venus barycenter'],
        'moon': eph['earth barycenter'],
        'mars': eph['mars barycenter'],
        'jupiter': eph['jupiter barycenter'],
        'saturn': eph['saturn barycenter'],
        'uranus': eph['uranus barycenter'],
        'neptune': eph['neptune barycenter'],
        'pluto': eph['pluto barycenter']
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


def calculate_aspects_for_natal_chart(transits):
    """Вычисляет аспекты между планетами."""
    aspects = {}
    aspect_definitions = {
        'conjunction': (0, 8), # Соединение: 0° ± 8°
        'opposition': (180, 8), # Оппозиция: 180° ± 8°
        'square': (90, 8), # Квадрат: 90° ± 8°
        'trine': (120, 8), # Тригон: 120° ± 8°
        'sextile': (60, 6) # Секстиль: 60° ± 6°
    }

    planet_names = list(transits.keys())
    dates = [time for time, _ in transits[planet_names[0]]]

    for i, date in enumerate(dates):
        daily_aspects = []
        planet_positions = {planet: transits[planet][i][1] for planet in planet_names}

        for j in range(len(planet_names)):
            for k in range(j + 1, len(planet_names)):
                planet1 = planet_names[j]
                planet2 = planet_names[k]
                angle = abs(planet_positions[planet1] - planet_positions[planet2]) % 360
                angle = min(angle, 360 - angle)

                for aspect_name, (ideal_angle, orb) in aspect_definitions.items():
                    if abs(angle - ideal_angle) <= orb:
                        daily_aspects.append((planet1, planet2, aspect_name))
                        break

        aspects[date.strftime('%Y-%m-%d %H:%M:%S')] = daily_aspects

    return aspects
