import socketio
import time
import curses
import numpy as np
import wcwidth

# Socket.IOクライアントのインスタンスを作成
sio = socketio.Client()

player_name = ""
stdscr = None  # グローバル変数として stdscr を宣言
last_goal_player = None


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

    def select_char(player_cell, field_cell):
        if player_cell == 1:
            return "😀"
        match field_cell:
            case 0:
                return "🌳"
            case 1:
                return "🗿"
            case 2:
                return "🎉"
            case _:
                return "🌳"

    global stdscr, last_goal_player
    player_map = data["player_map"]
    field = data["field"]
    if player_name == "":
        return
    if stdscr:
        stdscr.clear()
        for i, row in enumerate(zip(player_map, field)):
            col = 0
            for cell in zip(*row):
                char = select_char(*cell)
                if last_goal_player:
                    stdscr.addstr(1, 2, f"{last_goal_player}がゴールしました！！")
                stdscr.bkgd(" ", curses.color_pair(1) | curses.A_BOLD)
                stdscr.addstr(i + 2, col + 2, char)
                col += wcwidth.wcwidth(char)  # 文字の幅を考慮して位置を更新
        stdscr.refresh()
    else:
        print("Received response:", data)


@sio.event
def goal(name):
    global last_goal_player
    last_goal_player = name
    # global stdscr
    # if stdscr:
    #     stdscr.clear()  # 画面をクリア
    #     stdscr.addstr(15, 15, f"{name}がゴールしました！！")
    #     stdscr.refresh()  # 描画を更新

    # print(name)


def main(stdscr_main):
    global stdscr
    stdscr = stdscr_main

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
    while True:
        data = {"player_name": player_name, "dir": chr(stdscr.getch())}
        sio.emit("move", data)


if __name__ == "__main__":
    try:
        # サーバーに接続
        sio.connect("http://127.0.0.1:2500")

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
