import calendar
import pytz

from datetime import datetime

from skyfield.api import load
from skyfield.almanac import find_discrete, moon_phases

from core.config import eph
from core.models import MoonPhasesChoices, MoonEventsChoices


def get_moon_phases(year: int, start_month: int, end_month: int = 0, timezone=None) -> list:
    phases = moon_phases(eph)
    ts = load.timescale()
    if end_month == 0:
        end_month = start_month

    last_day_of_month = calendar.monthrange(year, start_month)[1]
    t_start = ts.utc(year, start_month, 1)
    t_end = ts.utc(year, end_month, last_day_of_month)

    times, phase_names = find_discrete(t_start, t_end, phases)

    mp = find_moon_phases(times, phase_names)
    blue_moons = find_blue_moons(mp)
    supermoons, micromoons = find_supermoons_and_micromoons(mp)

    lunar_schedule = []

    for date_time, phase in mp:
        """ important to know - situations when lunar events and moon phases have different times cannot be """
        moon_event = []

        if phase == MoonPhasesChoices.FULL_MOON and date_time.month == 1:
            moon_event.append(MoonEventsChoices.WOLFMOON.value)

        if date_time in blue_moons:
            moon_event.append(MoonEventsChoices.BLUE_MOON.value)

        if (date_time, phase) in supermoons:
            moon_event.append(MoonEventsChoices.SUPERMOON.value)

        if (date_time, phase) in micromoons:
            moon_event.append(MoonEventsChoices.MICROMOON.value)

        moon_phase_data = {
            "datetime": date_time.strftime('%Y-%m-%d %H:%M:%S'),
            "phase": phase,
        }

        if moon_event:
            moon_phase_data["events"] = moon_event
        lunar_schedule.append(moon_phase_data)

    return lunar_schedule


def find_moon_phases(times, phase_names):
    phases = []
    phase_labels = [MoonPhasesChoices.NEW_MOON, MoonPhasesChoices.FIRST_QUARTER,
                    MoonPhasesChoices.FULL_MOON, MoonPhasesChoices.THIRD_QUARTER
                    ]

    for t, phase in zip(times, phase_names):
        utc_time = t.utc_iso()
        utc_time_obj = datetime.strptime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
        utc_time_obj = pytz.utc.localize(utc_time_obj)

        phases.append((utc_time_obj, phase_labels[phase]))

    return phases


def find_blue_moons(phases):
    full_moons = [p[0] for p in phases if p[1] == MoonPhasesChoices.FULL_MOON]
    blue_moons = []
    current_month = None
    moon_count = 0

    for fm in full_moons:
        if current_month == fm.month:
            moon_count += 1
            if moon_count == 2:
                blue_moons.append(fm)
        else:
            current_month = fm.month
            moon_count = 1

    return blue_moons


def find_supermoons_and_micromoons(phases):
    moon = eph['moon']
    earth = eph['earth']

    supermoons, micromoons = [], []
    ts = load.timescale()
    for local_time, phase in phases:
        if phase == MoonPhasesChoices.FULL_MOON:
            t = ts.from_datetime(local_time) # координаты Земли и Луны в момент времени t

            astrometric_earth, astrometric_moon = earth.at(t), moon.at(t)
            distance = (astrometric_earth - astrometric_moon).distance()

            if distance.km < 361_857:
                supermoons.append((local_time, phase))

            if distance.km > 405_500:
                micromoons.append((local_time, phase))

    return supermoons, micromoons


def find_previous_new_moon(choosed_time: datetime) -> datetime:
    """finds the past new moon in UTC"""
    ts = load.timescale()

    t0 = ts.utc(choosed_time.year, choosed_time.month, choosed_time.day - 30)
    t1 = ts.utc(choosed_time.year, choosed_time.month, choosed_time.day + 1)

    phases = moon_phases(eph)
    times, phase_types = find_discrete(t0, t1, phases)

    for t, phase in zip(times, phase_types):
        if phase == 0 and t.utc_datetime() <= choosed_time:
            return t.utc_datetime()


def get_moon_cycle(choosed_time: datetime) -> int:
    """returns one of 30 moon cycles"""
    new_moon = find_previous_new_moon(choosed_time)

    days_since_new_moon = (choosed_time - new_moon).days + (choosed_time - new_moon).seconds / 86400
    current_day = round(days_since_new_moon % 29.53)

    return current_day


def get_current_lunar_phase(year: int, month: int, day: int) -> int:
    """gets the current lunar phase"""
    lunar_phases = get_moon_phases(year, month)

    target_date = datetime(year, month, day)

    for item in lunar_phases:
        item['datetime'] = datetime.strptime(item['datetime'], '%Y-%m-%d %H:%M:%S')

    closest_event = min(lunar_phases, key=lambda x: abs(x['datetime'] - target_date))['phase']

    return closest_event
