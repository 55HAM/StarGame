from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from core.connection import router as ws_router

BASE = Path(__file__).parent

app = FastAPI(title="HAM-FH")
app.include_router(ws_router)


@app.get("/")
async def lobby():
    return FileResponse(BASE / "static" / "index.html")


@app.get("/games/{game}/")
async def game_page(game: str):
    p = BASE / "games" / game / "index.html"
    if not p.exists():
        raise HTTPException(404, "لعبة غير موجودة")
    return FileResponse(p)