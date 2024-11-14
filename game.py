import numpy as np


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

        if 0 <= new_pos[0] < self.field.width and 0 <= new_pos[1] < self.field.height:
            player.set(new_pos)
            self.player_map.set(player.pos, 1)

            return

        self.player_map.set(player.pos, 1)

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

    def compile_layers(self):
        """
        クライアントに送るMap配列(fieldとplayer_mapを合わせたもの)
        を生成する
        """
        compiled_layer

    def print_field(self):
        """
        デバッグ用のプリント
        """
        print("Field:")
        print(self.field.array)
        print("\nPlayer Positions:")
        print(self.player_map.array)


if __name__ == "__main__":

    game = Game(width=10, height=10)

    for i in range(1, 9):
        game.place_object((i, 2), 1)
        game.place_object((i, 7), 1)

    game.add_player("adi", (3, 5))
    game.add_player("mio", (6, 5))

    game.print_field()
    print(game.players)

    game.move_player("adi", "w")
    game.move_player("adi", "a")
    game.move_player("mio", "a")
    game.print_field()

    game.delete_player("mio")
    game.print_field()
    print(game.players)
