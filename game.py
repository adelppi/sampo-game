import numpy as np
from scipy.ndimage import binary_dilation
from maze_generate import Maze


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.array = np.zeros(dtype=int, shape=(height, width))

    def set(self, pos, value):
        """
        Mapのposの座標に値をセットする
        """
        self.array[pos[1]][pos[0]] = value


class Player:
    def __init__(self, name, initial_x, initial_y):
        self.name = name
        self.x = initial_x
        self.y = initial_y

    @property
    def pos(self):
        """
        Playerのposを返す
            return: np.ndarray
        """
        return np.array([self.x, self.y])

    def set(self, pos):
        """
        Playerの位置をセットする
        """
        self.x = pos[0]
        self.y = pos[1]


class Game:
    def __init__(self, width, height):
        self.field = Map(width=width, height=height)
        self.player_map = Map(width=width, height=height)
        self.players = {}

    def add_player(self, name, initial_pos):
        """
        新しいPlayerを追加する
        """
        new_player = Player(name, initial_pos[0], initial_pos[1])
        self.players[name] = new_player
        self.place_player(new_player.pos)

    def is_movable(self, pos):
        """
        posの位置にプレイヤーが移動できるか
        """
        x, y = pos
        return (
            0 <= x < self.field.width
            and 0 <= y < self.field.height
            and self.field.array[y][x] != 1
        )

    def move_player(self, name, dir):
        """
        w, a, s, dをdirとして受け取って、指定したPlayerをその方向に動かす
        """

        def movement(d):
            match d:
                case "w":
                    return [0, -1]
                case "a":
                    return [-1, 0]
                case "s":
                    return [0, 1]
                case "d":
                    return [1, 0]
                case _:
                    return [0, 0]

        player = self.players[name]
        self.player_map.set(player.pos, 0)
        new_pos = player.pos + np.array(movement(dir))

        if self.is_movable(new_pos):
            player.set(new_pos)
            self.player_map.set(player.pos, 1)

            # if self.field.array[new_pos[1], new_pos[0]] == 2:
            #     print("goal")
            #     self.delete_player(name)

            return

        self.player_map.set(player.pos, 1)

    def place_pond_random(self, frequency):
        pond_array = np.zeros(dtype=int, shape=(self.field.height, self.field.width))

        indices = np.random.randint(
            0, self.field.height * self.field.width, size=frequency
        )
        pond_array.ravel()[indices] = 1
        dilated_pond_array = binary_dilation(
            pond_array, structure=np.ones((2, 2), dtype=int)
        )
        self.field.array = np.where(dilated_pond_array, 2, self.field.array)

    def generate_maze(self):
        """
        フィールドを迷路化する
        全ての値が迷路に上書きされる
        """
        maze = Maze(
            width=self.field.width, height=self.field.height, def_pos_y=1, def_pos_x=1
        )
        maze.main()
        self.field.array = np.array(maze.array)

    def place_object(self, pos, object):
        """
        指定したposにオブジェクトを置く
        """

        self.field.set(pos, object)

    def place_player(self, pos):
        """
        指定したposにPlayerを置く
        """
        self.player_map.set(pos, 1)

    def delete_player(self, name):
        """
        Playerを削除する
        """
        self.player_map.set(self.players[name].pos, 0)
        del self.players[name]

    def print_field(self):
        """
        デバッグ用のプリント
        """
        print("Field:")
        print(self.field.array)
        print("\nPlayer Positions:")
        print(self.player_map.array)


if __name__ == "__main__":

    game = Game(width=25, height=25)

    # game.place_pond_random(10)
    # for i in range(1, 9):
    #     game.place_object((i, 2), 1)
    #     game.place_object((i, 7), 1)

    game.generate_maze()

    game.print_field()
