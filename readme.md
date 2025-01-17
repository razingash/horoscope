

## QuickStart
1) In the backend directory run initialization command run the command to initialize the database
   ```bash 
    python manage.py initialization
   ```

2) to start the project as usual run
    ```bash 
    python main.py
   ```

## Description
Ordinary horoscope, with natal chart and lunar events

### Tech stack
- The goal of the project is to create a proper PWA application and publish it on the playmarket. ReactJS will be used for this purpose

- Backend is written in FastAPI, since it would be too easy and boring with Django, also it will be less effective

### Luna
calculation of the phases of the moon, and lunar events, such as blue moon, micromoon, full moon, wolf moon, etc. It is also planned to calculate eclipses

### Horoscope
horoscope - daily/weekly/monthly/yearly. 
- the calculation takes place depending on the zodiac sign, planet, house, aspect.
- -  the only problem is the large number of required patterns. It takes time to generate such a large number

#### horoscope variations
daily and annual horoscopes analyze data on a specific day, while monthly and weekly horoscopes analyze data over a period of time

1) daily
- for living zodiacs
- - zodiacs(12) * planets(10) * houses(12) * aspects(6) = 8640 * 3 = 25920
- for dead zodiacs (without planets in their fields)
- - zodiacs(12) * moon position(12) * moon monthly cycle(30) = 4320 * 3 = 12960
2) weekly
- for living zodiacs
- - zodiacs(12) * planets(10) * houses(12) * lunar phase(4)= 5760 * 3 = 17280
- for dead zodiacs
- - zodiacs(12) * where is the ruling planet(12) * houses(12) * lunar phase(4) = 6912 * 3 = 20736
3) monthly
- for living zodiacs
- - zodiacs(12) * planets(10) * houses(12) * seasons?(4)= 5760 * 3 = 17280
- for dead zodiacs
- - zodiacs(12) * where is the ruling planet(12) * houses(12) = 1728 * 3 = 5184
4) Annual

this forecast is based on the position of the planets at the beginning of the year
- for living zodiacs
- - zodiacs(12) * planets(10) * houses(12) = 1440 * 3 = 4320
- for dead zodiacs
- - zodiacs(12) * where is the ruling planet(12) * houses(12) = 1728 * 3 = 5184

### Natal chart
will be implemented before the patterns are uploaded to GitHub
