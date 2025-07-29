from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from main import Game

game = Game()
app = FastAPI()


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
async def create(height: int = 4, width: int = 4):
    game.create(height, width)


@app.post("/switch")
async def switch():
    game.switch()


@app.post("/check_if_complete")
async def check_if_complete(x, y):
    return game.check_if_complete(x, y)


@app.post("/check_all_squares")
async def check_all_squares():
    game.check_all_squares()


@app.post("/place_vertical")
async def place_vertical(x, y):
    return game.place_vertical(x, y)


@app.post("/place_horizontal")
async def place_horizontal(x, y):
    return game.place_horizontal(x, y)


@app.post("/get_winner")
async def get_winner():
    return game.get_winner()


@app.post("/undo")
async def undo():
    return game.undo()


@app.get("/is_valid_vertical_move")
async def is_valid_vertical_move(x, y):
    return game.is_valid_vertical_move(x, y)


@app.get("/is_valid_horizontal_move")
async def is_valid_horizontal_move(x, y):
    return game.is_valid_horizontal_move(x, y)


@app.get("/get_valid_moves")
async def get_valid_moves():
    return game.get_valid_moves()


@app.post("/make_move")
async def make_move(x, y, direction):
    return game.make_move(x, y, direction)


@app.get("/evaluate_position")
async def evaluate_position():
    return game.evaluate_position()


@app.get("/copy")
async def copy():
    return game.copy()


@app.get("/minimax")
async def minimax(depth, alpha, beta, maximizing):
    return game.minimax(depth, alpha, beta, maximizing)


@app.get("/get_best_move")
async def get_best_move(depth):
    return game.get_best_move(depth)
