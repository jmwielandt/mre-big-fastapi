import asyncio
import signal

from fastapi import APIRouter, FastAPI, Request
import hypercorn
from hypercorn.asyncio import serve
from starlette.middleware.base import BaseHTTPMiddleware


app = FastAPI()
router = APIRouter(prefix="/example")

STATE = 0  # dummy example


@router.get("/")
async def handle_example():
    print("I'm in!")
    return {"num_of_visits": STATE}


# middleware
async def log_request(request: Request, call_next):
    path = request.url.path
    method = request.method
    global STATE
    STATE += 1
    print(f"Logging request performed. Path={path!r}. Method={method!r}. State={STATE}")
    return await call_next(request)


def main():
    app.include_router(router)
    app.add_middleware(BaseHTTPMiddleware, dispatch=log_request)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    loop = asyncio.new_event_loop()

    cfg = hypercorn.Config()
    cfg.bind = "localhost:3000"

    server_coro = serve(app, cfg, shutdown_trigger=lambda: asyncio.Future())

    loop.create_task(server_coro)

    loop.run_forever()


if __name__ == "__main__":
    main()





