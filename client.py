import socketio

# Socket.IOクライアントのインスタンスを作成
sio = socketio.Client()

# 接続時のイベント
@sio.event
def connect():
    print("Connected to server")

# メッセージを受信したときのイベント
@sio.event
def response(data):
    print('Received response:', data)
    print()

# 切断時のイベント
@sio.event
def disconnect():
    print("Disconnected from server")

def main():
    # サーバーに接続
    sio.connect('http://127.0.0.1:5000')

    # メッセージを送信
    while True:
        message = input("Enter message to send (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        sio.emit('message', message)

    # 接続を切断
    sio.disconnect()

if __name__ == '__main__':
    main()
