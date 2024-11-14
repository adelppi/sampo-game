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
def response(data):
    global stdscr  # stdscr をグローバル変数として使用
    field = data["map"]
    if stdscr:
        for i, row in enumerate(field):
            for j, cell in enumerate(row):
                stdscr.addstr(i, j, "#" if cell == 1 else " ")
        # stdscr.refresh()
    else:
        print("Received response:", data)


def main(stdscr_main):
    global stdscr
    stdscr = stdscr_main  # main 関数の stdscr をグローバル変数に代入

    while True:
        match stdscr.getch():
            case 119:
                dir = "w"
            case 97:
                dir = "a"
            case 115:
                dir = "s"
            case 100:
                dir = "d"
            case _:
                continue

        data = {"player_name": player_name, "dir": dir}
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
