import random
import sys
from collections import deque
import numpy as np

sys.setrecursionlimit(10**6)

class maze:
    def __init__(self,width,height,def_pos_y,def_pos_x):
        self.width=width
        self.height=height
        self.array=np.ones((height,width),dtype=int)
        self.def_pos_x=def_pos_x
        self.def_pos_y=def_pos_y
        self.dx=[1,-1,0,0]  #x方向のベクトル
        self.dy=[0,0,1,-1]  #y方向のベクトル
    
    def set(self):
        self.array[self.def_pos_x,self.def_pos_y] = 0   #初期地点を掘削

    def make_maze(self,pos_y,pos_x):
        vector=list(range(4))
        random.shuffle(vector)  #ランダムに行く方向を決める

        for i in vector:
            ny=pos_y+self.dy[i]*2
            nx=pos_x+self.dx[i]*2

            if ny < 1 or ny >= self.height-1 or nx < 1 or nx >= self.width-1: #周りの壁を越えていたらスルー
                continue

            if self.array[ny][nx] == 0:   #2マス先が既に通路ならスルー
                continue

            #通路を掘る
            self.array[pos_y+self.dy[i]][pos_x+self.dx[i]]=0
            self.array[ny][nx]=0

            #再帰的に次の位置を掘る
            self.make_maze(ny,nx)

    def max_distance(self):
        q = deque([(self.def_pos_y, self.def_pos_x)])
        max_dist = 0        #最長距離
        goal_y, goal_x=self.def_pos_y,self.def_pos_x            #ゴール地点の初期化
        dist = [[-1]*self.width for _ in range(self.height)]    #それぞれのマスの距離を持つ配列
        dist[self.def_pos_y][self.def_pos_x] = 0

        while q:                #キューに要素がなくなるまで回す
            y,x = q.popleft()   #先頭から要素を取り出す
            for i in range(4):
                ny = y+self.dy[i]
                nx = x+self.dx[i]

                if ny < 0 or nx < 0 or ny >= self.height or nx >= self.width: #次に行くマスが壁だったらスルー
                    continue

                if self.array[ny][nx]==1 or dist[ny][nx] != -1: #次に行くマスが壁だったらスルー
                    continue

                q.append((ny,nx))
                dist[ny][nx] = dist[y][x]+1

                if dist[ny][nx] > max_dist: # 最長距離を更新
                    goal_y,goal_x = ny,nx
                    max_dist = dist[ny][nx]

        #ゴール地点を設定
        self.array[goal_y][goal_x] = 3
    
    def main(self):
        self.set()
        self.make_maze(pos_y=self.def_pos_y,pos_x=self.def_pos_x)
        self.max_distance()

maze_temp=maze(width=25,height=25,def_pos_y=1,def_pos_x=1)
maze_temp.main()

for i in maze_temp.array:
    print(*i)


