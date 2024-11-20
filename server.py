from flask import Flask
from flask_socketio import SocketIO, emit

from game import Game

import random

app = Flask(__name__)
socketio = SocketIO(app)

game = Game(width=25, height=25)

game.place_pond_random(20)

for i in range(1, 25):
    game.place_object((i, 2), 1)
    game.place_object((i, 7), 1)


@app.route("/")
def index():
    return {"statue": "online"}


@socketio.on("move")
def move(data):
    dir = data["dir"]
    player_name = data["player_name"]

    print(f"player: {player_name}, dir: {dir}")
    game.move_player(player_name, dir)
    print(game.player_map.array)
    emit(
        "response",
        {
            "player_map": game.player_map.array.tolist(),
            "field": game.field.array.tolist(),
        },
        broadcast=True,
    )


@socketio.on("join")
def join(player_name):
    game.add_player(player_name, (random.randint(0, 9), random.randint(0, 9)))
    game.print_field()


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=3000, debug=True)
