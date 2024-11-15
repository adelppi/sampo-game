import socketio
import time
import curses
import numpy as np

# Socket.IOクライアントのインスタンスを作成
sio = socketio.Client()

player_name = ""
stdscr = None  # グローバル変数として stdscr を宣言


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
def response(data: any):
    global stdscr
    field = data["map"]
    if stdscr:
        stdscr.clear()
        for i, row in enumerate(field):
            for j, cell in enumerate(row):
                stdscr.addstr(i, j, "😀" if cell == 1 else "🌳")
        stdscr.refresh()
    else:
        print("Received response:", data)


def main(stdscr_main):
    global stdscr
    stdscr = stdscr_main

    while True:
        data = {"player_name": player_name, "dir": chr(stdscr.getch())}
        sio.emit("move", data)


if __name__ == "__main__":
    try:
        # サーバーに接続
        sio.connect("http://127.0.0.1:5000")

        # ユーザーからメッセージを入力
        player_name = input("プレイヤー名を入力: ")
        sio.emit("join", player_name)

        # レスポンスを待つため少し待機
        time.sleep(1)

        curses.wrapper(main)

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # 接続を切断
        if sio.connected:
            sio.disconnect()
