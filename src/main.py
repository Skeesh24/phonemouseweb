import logging
from json import loads

import uvicorn
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from dependencies import get_broker
from interfaces import IBroker
from router import main_router

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    broker: IBroker = Depends(get_broker),
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")

            logging.info(data)

            if data == "connected":
                continue

            data = loads(data)

            if data["event"] == "devicemotion":
                broker.send(
                    ",".join(str(data["acceleration"][key]) for key in ("x", "y", "z")),
                )
            else:
                broker.send(
                    ",".join(str(data[key]) for key in ("alpha", "beta", "gamma")),
                )

    except WebSocketDisconnect:
        logging.info("WebSocket disconnected")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
