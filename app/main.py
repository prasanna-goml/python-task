from contextlib import asynccontextmanager
from datetime import datetime
import time

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.tickets import router
from app.api.ai import router as ai_router

from app.core.database import create_tables
from app.core.database import AsyncSessionLocal  # or see note below

from app.core.exceptions import TicketNotFoundError

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="AI Service Desk",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def response_time_middleware(request: Request, call_next):

    start = time.perf_counter()

    response = await call_next(request)

    end = time.perf_counter()

    elapsed = (end - start) * 1000

    response.headers["X-Response-Time"] = f"{elapsed:.0f}ms"

    return response

@app.exception_handler(TicketNotFoundError)
async def ticket_not_found_handler(
    request: Request,
    exc: TicketNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "error": "ticket_not_found",
            "id": exc.ticket_id,
        },
    )

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get(
    "/ready",
    tags=["Health"],
    status_code=status.HTTP_200_OK,
)
async def ready():

    checks = {}

    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))

        checks["database"] = "UP"

        return {
            "status": "READY",
            "checks": checks,
        }

    except SQLAlchemyError:

        checks["database"] = "DOWN"

        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "NOT_READY",
                "checks": checks,
            },
        )
from pyinstrument import Profiler
from fastapi import Request

@app.middleware("http")
async def profile_requests(request: Request, call_next):
    profiler = Profiler()
    profiler.start()

    response = await call_next(request)

    profiler.stop()

    print("\n" + "=" * 80)
    print(f"{request.method} {request.url.path}")
    print("=" * 80)
    print(profiler.output_text(unicode=True, color=True))

    return response
app.include_router(router)
app.include_router(ai_router)