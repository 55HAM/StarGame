from typing import Optional


class BaseRoom:
    """قالب كل غرفة لعبة. كل لعبة ترث وتعيد تعريف ما تحتاجه."""

    game_name: str = "base"

    def __init__(self, room_id: str):
        self.room_id = room_id
        self.players: dict = {}          # symbol -> {"pid": str, "ws": WebSocket}
        self.status: str = "waiting"     # waiting | playing | finished
        self.winner: Optional[str] = None

    def pid_symbol(self, pid: str) -> Optional[str]:
        for sym, p in self.players.items():
            if p["pid"] == pid:
                return sym
        return None

    def free_symbol(self) -> Optional[str]:
        return None

    def has_enough_players(self) -> bool:
        return len(self.players) >= 2

    def start_new_game(self) -> None:
        pass

    def state_for(self, symbol: str) -> dict:
        return {"type": "state"}

    async def handle_move(self, symbol: str, data: dict) -> None:
        pass

    async def broadcast(self) -> None:
        for sym, p in list(self.players.items()):
            try:
                await p["ws"].send_json(self.state_for(sym))
            except Exception:
                pass