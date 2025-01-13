

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
#### horoscope variation
1) for living zodiacs
- zodiacs(12) * planets(10) * houses(12) * aspects(5) = 7200
2) for dead zodiacs (without planets in their fields)
- ...

### Natal chart
will be implemented before the patterns are uploaded to GitHub
