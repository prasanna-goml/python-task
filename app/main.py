from contextlib import asynccontextmanager
from app.api.tickets import router
from app.core.database import create_tables
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import TicketNotFoundError
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(router)