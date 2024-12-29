import calendar
import json
import os
import pytz

from datetime import datetime
from skyfield.api import load
from skyfield.almanac import find_discrete, moon_phases

from core.config import MEDIA_DIR
from moon.constants import eph
from moon.crud import get_moon_schedule_path, add_moon_schedule


async def get_moon_phases(session, year, month): # CHANGE ?
    """а так ли надо хранить эти данные в базе данных, учитывая что основные данные хранятся, в json, а поля модели
        служат только для навигации по этим данным"""
    file_path = await get_moon_schedule_path(session, year, month) # DB

    if file_path is None:
        folder_path = os.path.join(MEDIA_DIR, f"moon/{year}")
        file_path = os.path.join(folder_path, f"{month}.json")
        print(folder_path, file_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        await add_moon_schedule(session, year=year, month=month, path=file_path)

    if not os.path.exists(file_path): # create json file with monthly data
        phases = moon_phases(eph)
        ts = load.timescale()

        last_day_of_month = calendar.monthrange(year, month)[1]
        t_start = ts.utc(year, month, 1)
        t_end = ts.utc(year, month, last_day_of_month)

        times, phase_names = find_discrete(t_start, t_end, phases)

        mp = find_moon_phases(times, phase_names)
        blue_moons = find_blue_moons(mp)
        supermoons, micromoons = find_supermoons_and_micromoons(mp)

        lunar_schedule = {
            "supermoons": [
                {"date": sm_time.strftime('%Y-%m-%d %H:%M:%S'), "phase": sm_phase} for sm_time, sm_phase in supermoons
            ],
            "micromoons": [
                {"date": sm_time.strftime('%Y-%m-%d %H:%M:%S'), "phase": sm_phase} for sm_time, sm_phase in micromoons
            ],
            "blue moons": blue_moons,
            "moon_phases": [
                {"time": time.strftime('%Y-%m-%d %H:%M:%S'), "phase": phase} for time, phase in mp
            ]
        }

        with open(file_path, 'w') as json_file:
            json.dump(lunar_schedule, json_file, indent=4, ensure_ascii=False)
    else:
        with open(file_path, 'r') as json_file:
            lunar_schedule = json.load(json_file)

    return lunar_schedule


def find_moon_phases(times, phase_names):
    phases = []
    phase_labels = ['New Moon', 'First Quarter', 'Full Moon', 'Last Quarter']

    for t, phase in zip(times, phase_names):
        utc_time = t.utc_iso()
        utc_time_obj = datetime.strptime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
        utc_time_obj = pytz.utc.localize(utc_time_obj)

        phases.append((utc_time_obj, phase_labels[phase]))

    return phases


def find_blue_moons(phases):
    full_moons = [p[0] for p in phases if p[1] == 'Full Moon']
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
        if phase == 'Full Moon':
            t = ts.from_datetime(local_time) # координаты Земли и Луны в момент времени t

            astrometric_earth, astrometric_moon = earth.at(t), moon.at(t)
            distance = (astrometric_earth - astrometric_moon).distance()

            if distance.km < 361_857: # приблизительная величина(мб найти точнее)
                supermoons.append((local_time, phase))

            if distance.km > 405_500:
                micromoons.append((local_time, phase))

    return supermoons, micromoons
