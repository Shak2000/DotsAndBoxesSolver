from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import Game

game = Game()
app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateGameRequest(BaseModel):
    height: int = 4
    width: int = 4


class MoveRequest(BaseModel):
    x: int
    y: int
    direction: str


class CheckCompleteRequest(BaseModel):
    x: int
    y: int


@app.get("/")
async def get_ui():
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")


@app.post("/create")
async def create(request: CreateGameRequest):
    try:
        print(f"Creating game with height={request.height}, width={request.width}")
        game.create(request.height, request.width)
        print("Game created successfully")
        print(f"Game state after creation:")
        print(f"  Height: {game.height}")
        print(f"  Width: {game.width}")
        print(f"  Remaining: {game.remaining}")
        print(f"  Winner: {game.get_winner()}")
        return {"success": True}
    except Exception as e:
        print(f"Error creating game: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/switch")
async def switch():
    try:
        game.switch()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/check_if_complete")
async def check_if_complete(request: CheckCompleteRequest):
    try:
        result = game.check_if_complete(request.x, request.y)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/check_all_squares")
async def check_all_squares():
    try:
        game.check_all_squares()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/place_vertical")
async def place_vertical(request: MoveRequest):
    try:
        result = game.place_vertical(request.x, request.y)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/place_horizontal")
async def place_horizontal(request: MoveRequest):
    try:
        result = game.place_horizontal(request.x, request.y)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get_winner")
async def get_winner():
    try:
        winner = game.get_winner()
        return {"winner": winner}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/undo")
async def undo():
    try:
        result = game.undo()
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/is_valid_vertical_move")
async def is_valid_vertical_move(x: int, y: int):
    try:
        result = game.is_valid_vertical_move(x, y)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/is_valid_horizontal_move")
async def is_valid_horizontal_move(x: int, y: int):
    try:
        result = game.is_valid_horizontal_move(x, y)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get_valid_moves")
async def get_valid_moves():
    try:
        moves = game.get_valid_moves()
        return {"moves": moves}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/make_move")
async def make_move(request: MoveRequest):
    try:
        result = game.make_move(request.x, request.y, request.direction)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/evaluate_position")
async def evaluate_position():
    try:
        score = game.evaluate_position()
        return {"score": score}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get_best_move")
async def get_best_move(depth: int):
    try:
        best_move = game.get_best_move(depth)
        return {"best_move": best_move}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/game_state")
async def get_game_state():
    """Get the current game state for the UI"""
    try:
        print("Getting game state...")
        winner = game.get_winner()
        print(f"Winner from game.get_winner(): {winner}")
        print(f"Remaining moves: {game.remaining}")
        print(f"Game active: {game.remaining > 0}")
        
        state = {
            "height": game.height,
            "width": game.width,
            "current_player": game.player,
            "score_a": game.A,
            "score_b": game.B,
            "remaining_moves": game.remaining,
            "winner": winner,
            "vertical_lines": game.vertical,
            "horizontal_lines": game.horizontal,
            "inner_squares": game.inner
        }
        print(f"Game state: {state}")
        return state
    except Exception as e:
        print(f"Error getting game state: {e}")
        raise HTTPException(status_code=400, detail=str(e))
