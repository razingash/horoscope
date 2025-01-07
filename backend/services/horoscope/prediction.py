from datetime import datetime

def select_more_suitable_aspects(horoscope_data):
    """selects more suitable planets for a particular zodiac sign, if necessary"""
    zodiac_planet_association = [
        [5, 1, 6, 10], # Aries ['Mars', 'Sun', 'Jupiter', 'Pluto']
        [3, 4, 7, 2],  # Taurus ['Venus', 'Moon', 'Saturn', 'Mercury']
        [2, 3, 8, 6],  # Gemini ['Mercury', 'Venus', 'Uranus', 'Jupiter']
        [4, 6, 9, 3],  # Cancer ['Moon', 'Jupiter', 'Neptune', 'Venus']
        [1, 6, 5, 2],  # Leo ['Sun', 'Jupiter', 'Mars', 'Mercury']
        [2, 7, 3],     # Virgo ['Mercury', 'Saturn', 'Venus']
        [3, 7, 2, 4],  # Libra ['Venus', 'Saturn', 'Mercury', 'Moon']
        [10, 5, 4, 9], # Scorpio ['Pluto', 'Mars', 'Moon', 'Neptune']
        [6, 1, 9, 5],  # Sagittarius ['Jupiter', 'Sun', 'Neptune', 'Mars']
        [7, 5, 3, 2],  # Capricorn ['Saturn', 'Mars', 'Venus', 'Mercury']
        [8, 7, 2, 3],  # Aquarius ['Uranus', 'Saturn', 'Mercury', 'Venus']
        [9, 6, 3, 4]   # Pisces ['Neptune', 'Jupiter', 'Venus', 'Moon']
    ]
    planet_positions = horoscope_data['planet_positions']
    planet_houses = horoscope_data['planet_houses']
    aspects = horoscope_data['aspects']
    suitable_aspects = []

    for sign, planets in planet_positions.items():
        sign += 1
        prioritized_planets = sorted(
            planets,
            key=lambda planet: zodiac_planet_association[sign].index(planet)
            if planet in zodiac_planet_association[sign] else len(zodiac_planet_association[sign])
        )

        primary_planet = prioritized_planets[0]
        planet_aspects = [aspect for aspect in aspects if primary_planet in aspect[:2]]

        prioritized_aspects = sorted(
            planet_aspects,
            key=lambda aspect: zodiac_planet_association[sign].index(
                aspect[1] if aspect[0] == primary_planet else aspect[0])
            if (aspect[1] if aspect[0] == primary_planet else aspect[0]) in zodiac_planet_association[sign] else len(
                zodiac_planet_association[sign])
        )

        best_aspect = prioritized_aspects[0]
        house = planet_houses[primary_planet]
        suitable_aspects.append({"zodiac": sign, "planet": primary_planet, "house": house, "aspect": best_aspect})

    return suitable_aspects


def calculate_ascendant(base_ascendant=0, location_offset=0): # defaul function for calculating ascendant
    """можно также добавить функцию для рассчета сцендента если нечего делать будет"""
    day_of_year = datetime.today().timetuple().tm_yday
    ascendant_change_per_day = 360 / 365

    ascendant_position = base_ascendant + (ascendant_change_per_day * day_of_year) + location_offset
    ascendant_position %= 360

    return ascendant_position


def get_zodiac_sign_and_house(elongation): #! Настроить location_offset в самом конце (или же сделать новую функцию)
    sign_index = int(elongation // 30) # same as in ZodiacsChoices + 1
    ascendant = calculate_ascendant(location_offset=0)

    house_position = (elongation - ascendant) % 360 # угол относительно асцендента
    house = int(house_position // 30) + 1 # same as in HousesChoices

    return sign_index, house


def generate_horoscope(transits):
    """Генерирует гороскоп на основе транзитов и аспектов между планетами."""
    data = {}
    aspect_definitions = {
        'conjunction': (0, 8),  # Соединение: 0° ± 8°
        'opposition': (180, 8),  # Оппозиция: 180° ± 8°
        'square': (90, 8),  # Квадрат: 90° ± 8°
        'trine': (120, 8),  # Тригон: 120° ± 8°
        'sextile': (60, 6)  # Секстиль: 60° ± 6°
    }

    planet_names = list(transits.keys())
    dates = [time for time, _ in transits[planet_names[0]]]

    for i, date in enumerate(dates):
        daily_aspects = []
        planet_positions = {planet: transits[planet][i][1] for planet in planet_names}

        planet_zodiacs, planet_houses = {}, {}
        for planet, position in planet_positions.items():
            sign, house = get_zodiac_sign_and_house(position)
            if sign not in planet_zodiacs:
                planet_zodiacs[sign] = []
            planet_zodiacs[sign].append(planet)
            planet_houses[planet] = house

        for j in range(len(planet_names)):
            for k in range(j + 1, len(planet_names)):
                planet1 = planet_names[j]
                planet2 = planet_names[k]
                angle = abs(planet_positions[planet1] - planet_positions[planet2]) % 360
                angle = min(angle, 360 - angle)

                for aspect_name, (ideal_angle, orb) in aspect_definitions.items():
                    if abs(angle - ideal_angle) <= orb:
                        daily_aspects.append((planet1, planet2, aspect_name))

        data[date] = {
            "planet_positions": planet_zodiacs,
            "planet_houses": planet_houses,
            "aspects": daily_aspects
        }

    elevated_data = {'daily horoscope': select_more_suitable_aspects(data[date]) for date in data}

    return elevated_data
