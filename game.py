import numpy as np


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.array = np.zeros(dtype=int, shape=(height, width))

    def set(self, pos, value):
        self.array[pos[1]][pos[0]] = value


class Player:
    def __init__(self, name, initial_x, initial_y):
        self.name = name
        self.x = initial_x
        self.y = initial_y

    @property
    def pos(self):
        return (self.x, self.y)

    @pos.setter
    def pos(self, new_pos):
        self.pos = new_pos


class Game:
    def __init__(self, width, height):
        self.field = Map(width=width, height=height)
        self.player_map = Map(width=width, height=height)
        self.players = {}

    def add_player(self, name, initial_x, initial_y):
        new_player = Player(name, initial_x, initial_y)
        self.players[name] = new_player
        self.place_player(new_player.pos)

    def place_object(self, pos, object):
        self.field.set(pos, object)

    def place_player(self, pos):
        self.player_map.set(pos, 1)

    def print_field(self):
        print("Field:")
        print(self.field.array)
        print("\nPlayer Positions:")
        print(self.player_map.array)


if __name__ == "__main__":

    game = Game(width=10, height=10)

    for i in range(1, 9):
        game.place_object((i, 2), 1)
        game.place_object((i, 7), 1)

    game.add_player("adi", 3, 5)
    game.add_player("mio", 6, 5)

    game.print_field()
    print(game.players)
