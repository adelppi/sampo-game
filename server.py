from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def index():
    return {"statue": "online"}


# イベントリスナーの例
@socketio.on("message")
def handle_message(message):
    print("Received message:", message)
    emit("response", {"msg": "Message received!"})  # クライアントに応答を送信


if __name__ == "__main__":
    socketio.run(app)
