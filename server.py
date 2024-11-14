from flask import Flask
from flask_socketio import SocketIO, emit

from game import Game

import random

app = Flask(__name__)
socketio = SocketIO(app)

game = Game(width=10, height=10)


@app.route("/")
def index():
    return {"statue": "online"}


@socketio.on("move")
def move(data):
    dir = data["dir"]
    player_name = data["player_name"]

    print(f"movement received: {dir}")
    game.move_player(player_name, dir)
    print(game.player_map.array)
    emit(
        "response", {"map": game.player_map.array.tolist()}
    )  # クライアントに応答を送信


@socketio.on("join")
def join(player_name):
    print("Received message:", player_name)
    emit("response", {"msg": "Message received!"})  # クライアントに応答を送信

    game.add_player(player_name, (random.randint(0, 9), random.randint(0, 9)))
    game.print_field()


if __name__ == "__main__":
    socketio.run(app)
