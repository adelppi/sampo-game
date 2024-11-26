import random
import sys
from collections import deque

sys.setrecursionlimit(10**6)

height, width = 31, 31
maze_base = [["#"]*width for _ in range(height)]

maze_base[1][1] = " " #初期地点
dx = [(1,2), (-1,-2), (0,0), (0,0)] #x軸のベクトル
dy = [(0,0), (0,0), (1,2), (-1,-2)] #y軸のベクトル

def make_maze(ny, nx):

    array = list(range(4)) 
    random.shuffle(array) #ランダムに行く方向を決める

    for i in array:

        if ny+dy[i][1]<1 or ny+dy[i][1]>=height: #周りの壁を越えていたらスルー
            continue

        if nx+dx[i][1]<1 or nx+dx[i][1]>=width: #周りの壁を越えていたらスルー
            continue

        if maze_base[ny+dy[i][1]][nx+dx[i][1]]==" ": #2つ先のマスがすでに開いていたらスルー
            continue

        for j in range(2): #通路を掘る
            maze_base[ny+dy[i][j]][nx+dx[i][j]] = " "

        make_maze(ny+dy[i][1], nx+dx[i][1]) #掘った先のところに移動

make_maze(1, 1)
maze_base[1][1] = "S"

sy=1    #初期スタート地点
sx=1    #同上
q = deque([(sy, sx)])
max_dist = 0 # 最長距離
gy, gx=1, 1 # ゴール地点
dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]
dist = [[-1]*width for _ in range(height)] # それぞれのマスの距離を持つ配列
dist[sy][sx] = 0

while q: # キューに要素がなくなるまで回す

    y,x = q.popleft() #先頭から要素を取り出す

    for i in range(4):

        ny = y+dy[i]
        nx = x+dx[i]

        if ny<=0 or nx<=0 or ny+1==height or nx+1==width: #次に行くマスが壁だったらスルー
            continue

        if maze_base[ny][nx]=="#": #次に行くマスが壁だったらスルー
            continue

        if dist[ny][nx]==-1: # まだ通っていなかったら距離を更新
            q.append((ny,nx))
            dist[ny][nx] = dist[y][x]+1

            if max_dist<dist[ny][nx]: # 最長距離を更新
                gy,gx = ny,nx
                max_dist = dist[ny][nx]

maze_base[gy][gx] = "G"

for i in maze_base:
    print(*i)
