from flask import Flask
from flask_socketio import SocketIO, emit

from game import Game

import random

app = Flask(__name__)
socketio = SocketIO(app)

game = Game(width=41, height=25)
game.generate_maze()


@app.route("/")
def index():
    return {"status": "online"}


@socketio.on("move")
def move(data):

    dir = data["dir"]
    player_name = data["player_name"]

    # すでにクリアしたプレイヤーからきた命令は無視する
    if player_name not in game.players.keys():
        return

    # print(f"player: {player_name}, dir: {dir}")
    game.move_player(player_name, dir)
    # print(game.player_map.array)

    player_pos = game.players[player_name].pos

    if game.field.array[player_pos[1], player_pos[0]] == 2:
        game.delete_player(name=player_name)
        print(player_name, "ゴール!!!!!!!!")
        emit(
            "goal",
            player_name,
            broadcast=True,
        )

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
    # game.add_player(player_name, (random.randint(0, 9), random.randint(0, 9)))
    game.add_player(player_name, (1, 1))
    game.print_field()


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=2500, debug=True)
