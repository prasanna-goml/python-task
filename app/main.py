from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.tickets import router
from app.core.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="AI Service Desk",
    lifespan=lifespan,
)

app.include_router(router)