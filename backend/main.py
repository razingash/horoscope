import argparse
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.middleware import add_cors_middleware
from apps.moon.router import router as moon_router
from apps.horoscope.router import router as horoscope_router
from apps.solar_system.router import router as ss_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("START")
    yield
    print('END')


app = FastAPI(lifespan=lifespan)

app.include_router(moon_router, prefix="/api/moon")
app.include_router(horoscope_router, prefix='/api/horoscope')
app.include_router(ss_router, prefix="/api/solar-system")

add_cors_middleware(app)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastAPI server")
    parser.add_argument("--addr", type=str, default="127.0.0.1:8000", help="Host and port to bind, e.g. 0.0.0.0:8000")
    args = parser.parse_args()

    host, port = args.addr.split(":")
    port = int(port)

    uvicorn.run("main:app", host=host, port=port, reload=True)
