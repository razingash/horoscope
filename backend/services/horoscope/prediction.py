import json
import os
from datetime import datetime

from core.config import MEDIA_DIR


def generate_horoscope(transits, horoscope_type: int):
    """Генерирует гороскоп на основе транзитов и аспектов между планетами."""
    if horoscope_type == 1:
        return horoscope_daily(transits)
    elif horoscope_type == 2:
        pass
    elif horoscope_type == 3:
        pass
    elif horoscope_type == 4:
        return horoscope_annual(transits)


def horoscope_daily(transits):
    data = {}
    aspect_definitions = {  # details in AspectsChoices
        1: (0, 8),  # conjunction: 0° ± 8°
        2: (180, 8),  # opposition: 180° ± 8°
        3: (90, 8),  # square: 90° ± 8°
        4: (120, 8),  # trine: 120° ± 8°
        5: (60, 6)  # sextile: 60° ± 6°
    }

    planet_names = list(transits.keys())
    dates = [time for time, _ in transits[planet_names[0]]]

    for i, date in enumerate(dates): #! когда решу как генерировать недельный и месячный убрать тут цикл
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

    elevated_data = {'horoscope': select_more_suitable_planet_with_aspect(data[date]) for date in data}

    return elevated_data


def horoscope_annual(transits):
    planet_names = list(transits.keys())
    #print(transits) # если и фиксить транзиты(временные значения) то только после гороскопов 2 типа
    planet_positions = {planet: transits[planet][0][1] for planet in planet_names}
    zodiac_planets, planet_house = {}, {}
    zodiac_house_shift = calculate_house_shift()

    for planet, position in planet_positions.items():
        sign, house = get_zodiac_sign_and_house(position)
        if sign not in zodiac_planets:
            zodiac_planets[sign] = []

        zodiac_planets[sign].append(planet)
        planet_house[planet] = house

    correlated_data = correlate_annual_horoscope_data(zodiac_planets, planet_house, zodiac_house_shift)
    return correlated_data


def correlate_annual_horoscope_data(zodiac_planets: dict, planet_house: dict, zodiac_house_shift: int) -> list:
    """correlates the positions of planets in the field of the zodiac sign or the main planet of the sign,
    if the sign is empty
    """

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

    new_zodiac_planets = {}
    for sign, planets in zodiac_planets.items():
        sign += 1
        prioritized_planets = sorted(
            planets,
            key=lambda planet: zodiac_planet_association[sign].index(planet)
            if planet in zodiac_planet_association[sign] else len(zodiac_planet_association[sign])
        )

        primary_planet = prioritized_planets[0]
        new_zodiac_planets[sign] = primary_planet

    new_data = []
    for i in range(1, 13):
        zodiac_planet = new_zodiac_planets.get(i)
        house = (i + zodiac_house_shift - 1) % 12 + 1
        if zodiac_planet:
            pattern = {
                "zodiac": i,
                "house": house,
                "planet": zodiac_planet,
            }
        else:
            primary_planet_for_sign = zodiac_planet_association[i - 1][0]
            house_position = planet_house.get(primary_planet_for_sign, None)

            pattern = {
                "zodiac": i,
                "house": house,
                "planet_position": house_position,  # Primary planet position of the sign
            }

        new_data.append(pattern)

    return new_data


def select_more_suitable_planet_with_aspect(horoscope_data): # позже возможно сделать из этой функции корелляцию, или задействовать её
    #! IMPROVE | сделать код для гороскопов 2 типа и ТОЛЬКО ПОТОМ начать менять это непотребство
    """selects more suitable planets and aspects for a particular zodiac sign, if necessary"""
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

        if planet_aspects:
            prioritized_aspects = sorted(
                planet_aspects,
                key=lambda aspect: zodiac_planet_association[sign].index(
                    aspect[1] if aspect[0] == primary_planet else aspect[0])
                if (aspect[1] if aspect[0] == primary_planet else aspect[0]) in zodiac_planet_association[sign]
                else len(zodiac_planet_association[sign])
            )
            best_aspect = prioritized_aspects[0][2]
        else:
            best_aspect = 0

        house = planet_houses[primary_planet]
        suitable_aspects.append({"zodiac": sign, "planet": primary_planet, "house": house, "aspect": best_aspect})

    return suitable_aspects


def calculate_house_shift():
    ascendant = calculate_ascendant()
    shift = ascendant % 360
    return int(shift // 30)


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


def document_prediction(year, month, day, horoscope_data, prediction_type) -> str:
    if prediction_type == 1: # daily
        folder_path = os.path.join(MEDIA_DIR, f"horoscope/daily/{year}/{month}")
        file_path = os.path.join(folder_path, f"{day}.json")
    elif prediction_type == 2: # weekly
        week_of_month = (day - 1) // 7 + 1
        folder_path = os.path.join(MEDIA_DIR, f"horoscope/weekly/{year}/{month}")
        file_path = os.path.join(folder_path, f"{week_of_month}.json")
    elif prediction_type == 3: # monthly
        folder_path = os.path.join(MEDIA_DIR, f"horoscope/monthly/{year}")
        file_path = os.path.join(folder_path, f"{month}.json")
    elif prediction_type == 4: # annual
        folder_path = os.path.join(MEDIA_DIR, f"horoscope/annual")
        file_path = os.path.join(folder_path, f"{year}.json")
    else:
        raise Exception('later improve')

    if not os.path.exists(folder_path): # create folder
        os.makedirs(folder_path)

    with open(file_path, 'w') as json_file: # create json file
        json.dump(horoscope_data, json_file, indent=2, ensure_ascii=False)

    return file_path
