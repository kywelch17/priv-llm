import httpx
import psycopg as pc
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import settings
from app.db import pool
from app.router import documents, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open()
    yield
    pool.close()

app = FastAPI(lifespan=lifespan)
app.include_router(documents.router)
app.include_router(health.router)
