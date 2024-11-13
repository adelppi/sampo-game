import socketio
import time

# Socket.IOクライアントのインスタンスを作成
sio = socketio.Client()


# 接続時のイベント
@sio.event
def connect():
    print("Connected to server")


# 切断時のイベント
@sio.event
def disconnect():
    print("Disconnected from server")


# メッセージを受信したときのイベント
@sio.event
def response(data):
    print("Received response:", data["msg"])


def main():
    try:
        # サーバーに接続
        sio.connect("http://127.0.0.1:5000")
        
        # ユーザーからメッセージを入力
        message = input("Enter message: ")
        sio.emit("message", message)
        
        # レスポンスを待つため少し待機
        time.sleep(1)
        
    except Exception as e:
        print(f"Error occurred: {e}")
    
    finally:
        # 接続を切断
        if sio.connected:
            sio.disconnect()

if __name__ == "__main__":
    main()
