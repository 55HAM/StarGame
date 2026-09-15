from core.base_room import BaseRoom

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


class XORoom(BaseRoom):
    game_name = "xo"

    def __init__(self, room_id: str):
        super().__init__(room_id)
        self.board = [None] * 9
        self.turn = "X"

    def free_symbol(self):
        for s in ("X", "O"):
            if s not in self.players:
                return s
        return None

    def start_new_game(self):
        self.board = [None] * 9
        self.turn = "X"
        self.winner = None
        self.status = "playing"

    def state_for(self, symbol):
        return {
            "type": "state",
            "board": list(self.board),
            "turn": self.turn,
            "status": self.status,
            "winner": self.winner,
            "yourSymbol": symbol,
            "connected": {s: (s in self.players) for s in ("X", "O")},
        }

    async def handle_move(self, symbol, data):
        if self.status != "playing" or symbol != self.turn:
            return
        idx = data.get("index")
        if not isinstance(idx, int) or not (0 <= idx < 9):
            return
        if self.board[idx] is not None:
            return

        self.board[idx] = symbol
        w = self._check_winner()
        if w:
            self.winner = w
            self.status = "finished"
        else:
            self.turn = "O" if self.turn == "X" else "X"
        await self.broadcast()

    def _check_winner(self):
        for a, b, c in LINES:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        if all(self.board):
            return "draw"
        return None