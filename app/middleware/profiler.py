from pathlib import Path
from fastapi import Request
from pyinstrument import Profiler

LOG_FILE = Path("logs/profiler.log")
LOG_FILE.parent.mkdir(exist_ok=True)


async def profile_requests(request: Request, call_next):
    profiler = Profiler()
    profiler.start()

    response = await call_next(request)

    profiler.stop()

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 80 + "\n")
        f.write(f"{request.method} {request.url.path}\n")
        f.write("=" * 80 + "\n")
        f.write(profiler.output_text(unicode=True, color=False))
        f.write("\n")

    return response