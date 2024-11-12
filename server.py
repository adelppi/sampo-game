from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

# イベントリスナーの例
@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    emit('response', {'data': 'Message received!'})  # クライアントに応答を送信

if __name__ == '__main__':
    socketio.run(app)
