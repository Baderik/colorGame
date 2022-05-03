from fastapi import Request, APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from core import manager
from settings import TEMPLATES_DIR
from services import proc_request, disconnect_message, r_color, change_partner

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "color": r_color()})


@router.websocket("/ws",)
async def websocket_endpoint(websocket: WebSocket):
    my_ws = await manager.connect(websocket)
    await manager.send_data(my_ws.ws_id, {"type": "start", "data": my_ws.ws_id})
    await change_partner(my_ws.ws_id)
    await manager.send_online()

    try:
        while True:
            data: str = await websocket.receive_text()
            await proc_request(my_ws.ws_id, data)

    except WebSocketDisconnect:
        manager.disconnect(my_ws.ws_id)
        await disconnect_message(my_ws)

    except ValidationError:
        print("WARNING | WS Invalid request type ws_id:", my_ws.ws_id)
