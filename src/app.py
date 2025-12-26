from fastapi import FastAPI
from config.settings import settings

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version="0.1.0",
)
