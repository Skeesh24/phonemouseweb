import asyncio
import logging
import random

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from dependencies import get_broker
from interfaces import IBroker

main_router = APIRouter(
    prefix="/api",
    tags=["API"],
)


async def event_generator(
    broker: IBroker,
):
    while True:
        await asyncio.sleep(0.01)  # задержка

        # получение данных из брокера сообщений
        data = broker.receive()

        if not data:
            continue

        yield f"data: {data}\n\n"


@main_router.get(
    "/sse/",
)
async def sse(
    broker: IBroker = Depends(get_broker),
):
    return StreamingResponse(
        event_generator(broker),
        media_type="text/event-stream",
    )
