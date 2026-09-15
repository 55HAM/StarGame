import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from games import GAMES

router = APIRouter()
rooms: dict = {}

GRACE_PERIOD = 90  # ثوانٍ تبقى فيها الغرفة حيّة بعد خلوّها


async def _cleanup_room_after(key, seconds: int):
    await asyncio.sleep(seconds)
    room = rooms.get(key)
    if room and not room.players:
        rooms.pop(key, None)


@router.websocket("/ws/{game}/{room_id}")
async def ws_endpoint(ws: WebSocket, game: str, room_id: str):
    await ws.accept()

    RoomClass = GAMES.get(game)
    if RoomClass is None:
        await ws.send_json({"type": "error", "message": "لعبة غير معروفة"})
        await ws.close()
        return

    room_id = room_id.upper().strip()
    pid = ws.query_params.get("pid") or "anon"
    key = (game, room_id)

    room = rooms.get(key)
    if room is None:
        room = RoomClass(room_id)
        rooms[key] = room

    # إذا عاد اللاعب نفسه، أعِد له رمزه القديم
    sym = room.pid_symbol(pid)
    if sym is None:
        sym = room.free_symbol()
        if sym is None:
            await ws.send_json({"type": "error", "message": "الغرفة ممتلئة"})
            await ws.close()
            return

    # اطرد أي اتصال قديم لنفس الرمز
    old = room.players.get(sym)
    if old and old["ws"] is not ws:
        try:
            await old["ws"].close()
        except Exception:
            pass

    room.players[sym] = {"pid": pid, "ws": ws}

    # ابدأ لعبة جديدة فقط إذا كانت الغرفة في حالة انتظار فعلية
    if room.has_enough_players() and room.status == "waiting":
        room.start_new_game()

    await room.broadcast()

    try:
        while True:
            data = await ws.receive_json()
            t = data.get("type")

            if t == "move":
                await room.handle_move(sym, data)

            elif t == "reset":
                if room.status == "finished" and room.has_enough_players():
                    room.start_new_game()
                    await room.broadcast()

    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        cur = room.players.get(sym)
        if cur and cur["ws"] is ws:
            del room.players[sym]

        # لا نغيّر حالة اللعبة إطلاقًا
        await room.broadcast()

        # إذا خلت الغرفة، جدول حذفها بعد مهلة السماح
        if not room.players:
            asyncio.create_task(_cleanup_room_after(key, GRACE_PERIOD))