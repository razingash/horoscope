import json
import os
from asyncio import run as asyncio_run

from colorama import Fore, Style

from .makemigrations import command_makemigrations
from .migrate import command_migrate
from core.database import db_session
from core.config import BASE_DIR
from core.models import HoroscopeFitDaily, HoroscopeVoidDaily, HoroscopeFitWeekly, HoroscopeVoidWeekly, \
    HoroscopeFitMonthly, HoroscopeVoidMonthly, HoroscopeFitAnnual, HoroscopeVoidAnnual, \
    HousesChoices, PlanetsChoices, AspectsChoices, ZodiacsChoices, LanguagesChoices, MoonPhasesChoices, EarthSeasons


def command_initialization():
    command_makemigrations()
    command_migrate()
    asyncio_run(generate_static_data())


async def fill_static_data_without_fixtures():
    async with db_session.session_factory() as session:
        batch_counter = 0

        async def commit_if_batch_full():
            nonlocal batch_counter
            if batch_counter >= 1000:
                await session.commit()
                batch_counter = 0

        def create_horoscope_entry(language, description, zodiac, model_class, **kwargs):
            nonlocal batch_counter
            horoscope = model_class(
                language=language, zodiac=zodiac, description=description, **kwargs
            )
            session.add(horoscope)
            batch_counter += 1

        for language in LanguagesChoices:
            for zodiac in ZodiacsChoices:
                for house in HousesChoices:
                    for planet in PlanetsChoices:
                        # annual
                        description = f'annual horoscope for {language.value}-{zodiac.value}-' \
                                      f'{planet.value}-{house.value}'
                        create_horoscope_entry(language, description, zodiac, HoroscopeFitAnnual,
                                               house=house, planet=planet)

                        await commit_if_batch_full()
                        for aspect in AspectsChoices:
                            # daily
                            description = f'daily horoscope for {language.value}-{zodiac.value}-' \
                                          f'{planet.value}-{house.value}-{aspect.value}'
                            create_horoscope_entry(language, description, zodiac, HoroscopeFitDaily,
                                                   house=house, planet=planet, aspect=aspect)

                            await commit_if_batch_full()
                        for lunar_phase in MoonPhasesChoices:
                            # weekly
                            description = f'weekly horoscope for {language.value}-{zodiac.value}-' \
                                          f'{planet.value}-{house.value}-{lunar_phase.value}'
                            create_horoscope_entry(language, description, zodiac, HoroscopeFitWeekly,
                                                   house=house, planet=planet, lunar_phase=lunar_phase)

                            await commit_if_batch_full()
                        for season in EarthSeasons:
                            # monthly
                            description = f'monthly horoscope for {language.value}-{zodiac.value}-' \
                                          f'{planet.value}-{house.value}-{EarthSeasons(season)}'
                            create_horoscope_entry(language, description, zodiac, HoroscopeFitMonthly,
                                                   house=house, planet=planet, season=season)

                            await commit_if_batch_full()
                    for main_planet in ZodiacsChoices:
                        # monthly void
                        description = f'annual horoscope for {language.value}-{zodiac.value}-' \
                                      f'{planet.value}-{house.value}-{main_planet.value}'
                        create_horoscope_entry(language, description, zodiac, HoroscopeVoidMonthly,
                                               house=house, main_planet_position=main_planet)

                        # annual void
                        description = f'monthly horoscope for {language.value}-{zodiac.value}-' \
                                      f'{planet.value}-{house.value}-{main_planet.value}'
                        create_horoscope_entry(language, description, zodiac, HoroscopeVoidAnnual,
                                               house=house, main_planet_position=main_planet)

                        await commit_if_batch_full()
                        for lunar_phase in MoonPhasesChoices:
                            # weekly void
                            description = f'weekly horoscope for {language.value}-{zodiac.value}-' \
                                          f'{planet.value}-{house.value}-{main_planet.value}-{lunar_phase.value}'
                            create_horoscope_entry(language, description, zodiac, HoroscopeVoidWeekly,
                                                   house=house, main_planet_position=main_planet, lunar_phase=lunar_phase)

                            await commit_if_batch_full()
                for i in range(1, 31):
                    # daily void
                    description = f'daily horoscope for {language.value}-{zodiac.value}-' \
                                  f'{planet.value}-{house.value}-lunar staget {i}'
                    create_horoscope_entry(language, description, zodiac, HoroscopeVoidDaily, moon_cycle=i)

                    await commit_if_batch_full()

        await session.commit()


async def fill_static_data_with_fixtures(fixtures_dir, file_names):
    async with db_session.session_factory() as session:
        try:
            ...
        except Exception as e:
            await session.rollback()
            return e
        else:
            return True


async def generate_static_data():
    print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + 'generating static data')

    fixtures_dir = os.path.join(BASE_DIR, 'fixtures', 'horoscope', 'daily')
    file_names = ['1_aries', '2_taurus', '3_gemini', '4_cancer', '5_leo', '6_virgo', '7_libra', '8_scorpius',
                  '9_saggitarius', '10_capricornus', '11_aquarius', '12_pisces']
    files = []
    try:
        for file_name in file_names:
            file_path = os.path.join(fixtures_dir, f"{file_name}.json")
            if not os.path.exists(file_path):
                files.append(file_path)
        if len(files) > 0:
            raise FileNotFoundError
    except FileNotFoundError:
        print([file for file in files], sep='\n')
        print(Style.BRIGHT + Fore.RED + 'not all fixtures are defined')
        print('Values will be replaced with test ones')
        await fill_static_data_without_fixtures() # если возникнет sqlalchemy.exc.IntegrityError то бд уже создана(странно)
        print(Style.BRIGHT + Fore.GREEN + 'Static data generation has been completed')
    else:
        try:
            result = await fill_static_data_with_fixtures(fixtures_dir, file_names)
            if result:
                print(Style.BRIGHT + Fore.GREEN + 'Static data generation has been completed')
        except Exception as e:
            print(f'Exception:\n{e}')
            print(Fore.RED + "static data was not generated due to an error in the fixtures")
