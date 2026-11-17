from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db import pool
from app.router import documents, health, chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open()
    yield
    pool.close()

app = FastAPI(lifespan=lifespan)
app.include_router(documents.router)
app.include_router(health.router)
app.include_router(chat.router)
