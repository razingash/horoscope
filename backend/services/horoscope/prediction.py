

def get_zodiac_sign(elongation):
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn",
        "Aquarius", "Pisces"
    ]
    sign_index = int(elongation // 30)
    return signs[sign_index]

# добавить еще ебучий выбор более весомой планеты если в одном знаке сразу несколько их
def generate_horoscope(transits): #!нужно также сгенерировать случаи, когда у зодиака нет планеты
    """Генерирует гороскоп на основе транзитов и аспектов между планетами."""
    horoscope = {}
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

        planet_zodiacs = {planet: get_zodiac_sign(planet_positions[planet]) for planet in planet_positions}

        for j in range(len(planet_names)):
            for k in range(j + 1, len(planet_names)):
                planet1 = planet_names[j]
                planet2 = planet_names[k]
                angle = abs(planet_positions[planet1] - planet_positions[planet2]) % 360
                angle = min(angle, 360 - angle)

                for aspect_name, (ideal_angle, orb) in aspect_definitions.items():
                    if abs(angle - ideal_angle) <= orb:
                        daily_aspects.append((planet1, planet2, aspect_name))

        horoscope[date.strftime('%Y-%m-%d %H:%M:%S')] = {
            "planet_positions": planet_zodiacs,
            "aspects": daily_aspects
        }

    return horoscope

