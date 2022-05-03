from random import randint

from core import manager, MyWS
from pd_model import StandardModel


async def disconnect_message(ws: MyWS) -> None:
    if ws.partner:
        response: StandardModel = StandardModel(type="disconnectPartner",
                                                data="We are looking for a new partner")
        await manager.set_partner(ws.partner)
        await manager.send_data(ws.partner, response.dict())
    await manager.send_online()


async def proc_request(ws_id: str, data: str) -> None:
    if data == "changePartner":
        await change_partner(ws_id)

    elif data == "changeColor":
        await _change_color(ws_id)


def r_color() -> str:
    return '#%02X%02X%02X' % (randint(0, 255), randint(0, 255), randint(0, 255))


async def change_partner(ws_id: str) -> None:
    ws: MyWS = await manager.get_ws(ws_id)
    partner_id: str = await manager.find_partner(ws_id, ws.partner)
    if ws.partner:
        await manager.set_partner(ws.partner)
        response: StandardModel = StandardModel(type="disconnectPartner",
                                                data="We are looking for a new partner")
        await manager.send_data(ws.partner, response.dict())

    await manager.set_partner(ws_id, partner_id)

    if partner_id:
        response: StandardModel = StandardModel(type="changePartner", data=ws_id)
        await manager.set_partner(partner_id, ws_id)
        await manager.send_data(partner_id, response.dict())
        response.data = partner_id

    else:
        response: StandardModel = StandardModel(type="disconnectPartner",
                                                data="We are looking for a new partner")
    await manager.send_data(ws.ws, response.dict())


async def _change_color(ws_id: str) -> None:
    ws: MyWS = await manager.get_ws(ws_id)

    if ws.partner:
        response: StandardModel = StandardModel(type="changeColor", data=r_color())
        await manager.send_data(ws.partner, response.dict())
    else:
        response: StandardModel = StandardModel(type="message",
                                                data="You haven't a partner, "
                                                     "you can't change a color")
        await manager.send_data(ws_id, response.dict())
