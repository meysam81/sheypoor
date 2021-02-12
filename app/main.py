from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import api
from app.core.config import config

app = FastAPI(title="Sheypoor")

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix=config.API_URI)
