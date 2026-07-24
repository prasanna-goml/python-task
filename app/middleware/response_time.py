import time

from fastapi import Request


async def response_time_middleware(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    elapsed = (time.perf_counter() - start) * 1000
    response.headers["X-Response-Time"] = f"{elapsed:.0f}ms"

    return response