from fastapi import FastAPI
from .moon.router import router as moon_router

app = FastAPI()

app.include_router(moon_router, prefix="/moon")
