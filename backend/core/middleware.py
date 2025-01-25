
from fastapi.middleware.cors import CORSMiddleware

#from main import app
def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
"""оставить тут только ситуативные мидлвейры, а остальные перенести на уровень nginx"""
