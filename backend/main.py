import asyncio
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.middleware import add_cors_middleware
from moon.router import router as moon_router
from horoscope.router import router as horoscope_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("START")
    yield
    print('END')


app = FastAPI(lifespan=lifespan)

app.include_router(moon_router, prefix="/moon")
app.include_router(horoscope_router, prefix='/horoscope')

add_cors_middleware(app)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    uvicorn.run("main:app", reload=True)
