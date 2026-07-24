from fastapi import Request
from pyinstrument import Profiler


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