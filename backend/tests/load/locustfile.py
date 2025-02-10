from locust import HttpUser, task, between

""" to load tests run 'locust -f locustfile.py' """


class HoroscopeTasks(HttpUser):
    wait_time = between(1, 2)
    host = "http://localhost:8080/api"

    @task
    def horoscope_daily(self):
        self.client.get("/horoscope/daily/")

    @task
    def horoscope_weekly(self):
        self.client.get("/horoscope/weekly/")

    @task
    def horoscope_monthly(self):
        self.client.get("/horoscope/monthly/")

    @task
    def horoscope_annual(self):
        self.client.get("/horoscope/annual/")

'''
class MoonPhasesTasks(HttpUser):
    """пока что этот апи будет уничтожен при множестве одновременных асинхронных запросов на одно и то же значение.
    Позже будет добавлено кэширование json ответов для nginx. Хоть это и решит проблему, но всегда так делать не получится,
    и придется делать дополнительные проверки в базе данных перед созданием новых, то есть, все запрсоы должны быть 
    идемпотентыми, что довольно сильно подкашивает асинхронный orm"""
    
    wait_time = between(1, 10)
    host = "http://localhost:8000"

    @task
    def moon_phases(self):
        year = random.randint(2000, 2030)
        month = random.randint(1, 12)

        self.client.get(f"/moon/lunar-forecast/{year}/{month}")
'''
