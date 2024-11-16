import asyncio
import random

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

main_router = APIRouter(
    prefix="/api",
    tags=["API"],
)

current_state = (0, 0, 0)


async def event_generator():
    global current_state
    while True:
        await asyncio.sleep(0.001)  # Имитация задержки
        # Генерация новых данных
        current_state = (
            random.randint(100, 100),
            random.randint(100, 500),
            random.randint(100, 500),
        )
        yield f"data: {current_state[0]},{current_state[1]},{current_state[2]}\n\n"


@main_router.get(
    "/sse/",
)
async def sse():
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
