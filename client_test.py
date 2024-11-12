import socketio
import msvcrt

# Socket.IOクライアントのインスタンスを作成
sio = socketio.Client()

# 接続時のイベント
@sio.event
def connect():
    print("Connected to server")

# メッセージを受信したときのイベント
@sio.event
def response(data):
    #渡された配列の内容を表示(後で改造)
    print(data)
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
        key=msvcrt.getwch()  #key入力を検知
        if key=='q':
            break
        sio.emit('message',key) #内容を送信

    # 接続を切断
    sio.disconnect()

if __name__ == '__main__':
    main()
