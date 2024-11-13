from flask import Flask
from flask_socketio import SocketIO, emit

from game import Game

app = Flask(__name__)
socketio = SocketIO(app)

game = Game(width=10, height=10)


@app.route("/")
def index():
    return {"statue": "online"}


@socketio.on("move")
def move(dir):
    print(f"movement received: {dir}")
    game.move_player("adi", dir)
    game.print_field()
    emit("response", {"msg": f"movement received: {dir}"})  # クライアントに応答を送信


@socketio.on("join")
def join(player_name):
    print("Received message:", player_name)
    emit("response", {"msg": "Message received!"})  # クライアントに応答を送信

    game.add_player(player_name, (2, 2))
    game.print_field()


if __name__ == "__main__":
    socketio.run(app)
