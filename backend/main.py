from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.database import create_database, delete_database
from moon.router import router as moon_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database()
    print("База готова")
    yield
    await delete_database()
    print('очистка')


app = FastAPI(lifespan=lifespan)

app.include_router(moon_router, prefix="/moon")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
