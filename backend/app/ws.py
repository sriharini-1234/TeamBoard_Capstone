import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .security import verify_token

router = APIRouter()
class ConnectionManager:
    def __init__(self):
        self.active = set()

    async def connect(self, ws):
        self.active.add(ws)

    def disconnect(self, ws):
        self.active.discard(ws)

    async def broadcast(self, event):
        for ws in list(self.active):
            try:
                await ws.send_json(event)
            except Exception:
                self.disconnect(ws)

manager = ConnectionManager()

@router.websocket("/ws/tickets")
async def tickets_ws(ws: WebSocket):
    await ws.accept()
    try:
        first = await asyncio.wait_for(ws.receive_json(), timeout=5)
        verify_token(first.get("token", ""))
        await manager.connect(ws)
        await ws.send_json({"type": "ready"})
        while True:
            await ws.receive_text()
    except (Exception, WebSocketDisconnect):
        try:
            await ws.close(code=1008)
        except Exception:
            pass
    finally:
        manager.disconnect(ws)
