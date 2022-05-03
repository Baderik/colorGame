from fastapi import FastAPI
from fastapi import WebSocket
from typing import Union
from uuid import uuid4


class MyWS:
    ws: WebSocket
    ws_id: str
    partner: str

    def __init__(self, ws: WebSocket, ws_id: str, partner: str = ""):
        self.ws = ws
        self.ws_id = ws_id
        self.partner = partner


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, MyWS] = {}

    async def connect(self, websocket: WebSocket) -> MyWS:
        await websocket.accept()
        ws_id = str(uuid4())
        self.active_connections[ws_id] = MyWS(websocket, ws_id)
        return self.active_connections[ws_id]

    def disconnect(self, websocket: Union[WebSocket, str]):
        if type(websocket) is str:
            del self.active_connections[websocket]
            return

        for key, item in self.active_connections.items():
            if item == websocket:
                del self.active_connections[key]
                return

    async def send_data(self, websocket: Union[str, WebSocket], response_dict: dict) -> None:
        if type(websocket) is str:
            websocket: WebSocket = self.active_connections[websocket].ws

        await websocket.send_json(response_dict)

    async def get_ws(self, ws_id: str) -> MyWS:
        return self.active_connections[ws_id]

    async def find_partner(self, ws_id: str, exclude: str = None) -> str:
        for partner_id, ws in self.active_connections.items():
            if partner_id == exclude or partner_id == ws_id or ws.partner:
                continue

            return partner_id
        return ""

    async def set_partner(self, f_id: str, s_id: str = ""):
        self.active_connections[f_id].partner = s_id

        if s_id:
            self.active_connections[s_id].partner = f_id

    async def send_online(self):
        count: int = len(self.active_connections)

        for my_ws in self.active_connections.values():
            await my_ws.ws.send_json({"type": "online", "data": count})



app = FastAPI()
manager = ConnectionManager()
