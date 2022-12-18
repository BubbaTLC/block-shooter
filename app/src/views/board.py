import random
import pyglet


class Tile(pyglet.shapes.Rectangle):
    def __init__(self,
                 x_index: int = 0,
                 y_index: int = 0,
                 *args: str,
                 **kwargs: int):
        super(Tile, self).__init__(*args, **kwargs)
        self.color = (58, 58, 58)
        # self.has_player = False
        # self.has_enemy = False
        self.x_index = x_index
        self.y_index = y_index


class Board():
    def __init__(self,
                 width: int,
                 height: int,
                 batch: pyglet.graphics.Batch = None) -> None:
        self.width: int = width
        self.height: int = height
        self.batch = batch
        self.tile_count_x: int = 5
        self.tile_count_y: int = 5
        self.padding: int = 5
        self.tile_positions: list[list[tuple]] = self.get_2d_matrix(
            self.tile_count_y, self.tile_count_x
        )
        self.tiles: list[list[Tile]] = self.get_2d_matrix(
            self.tile_count_y, self.tile_count_x
        )
        self.tiles
        self.load_tile_positions()
        self.create_tiles()

    def get_2d_matrix(self, rows: int, columns: int) -> list[list]:
        return [
            [None for _ in range(columns)]
            for _ in range(rows)
        ]

    def load_tile_positions(self) -> None:
        total_padding_x = self.padding * (self.tile_count_x + 1)
        total_padding_y = self.padding * (self.tile_count_y + 1)
        available_width = self.width - total_padding_x
        available_height = self.height - total_padding_y
        self.tile_width = int(available_width / self.tile_count_x)
        self.tile_height = int(available_height / self.tile_count_y)

        for i in range(self.tile_count_y - 1, -1, -1):
            for j in range(self.tile_count_x):
                x = j * self.tile_width + (j + 1) * self.padding
                y = i * self.tile_height + (i + 1) * self.padding
                self.tile_positions[i][j] = (x, y)

    def create_tiles(self) -> None:
        for i in range(self.tile_count_y - 1, -1, -1):
            for j in range(self.tile_count_x):
                x, y = self.tile_positions[i][j]
                self.tiles[i][j] = Tile(x=x,
                                        y=y,
                                        x_index=j,
                                        y_index=i,
                                        height=self.tile_height,
                                        width=self.tile_width,
                                        batch=self.batch)

    def get_random_tile(self) -> tuple:
        random_x = random.randint(0, self.tile_count_x-1)
        random_y = random.randint(0, self.tile_count_y-1)
        return self.tile_positions[random_x][random_y]

    def update(self) -> None:
        pass

    def get_offset(self) -> tuple:
        return (self.tile_width//2, self.tile_height//2)

    def get_size(self) -> tuple:
        return (self.width, self.height)

    # def get_player_tile(self) -> Tile:
    #     for i in range(self.tile_count_y - 1, -1, -1):
    #         for j in range(self.tile_count_x):
    #             if self.tiles[j][i].has_player:
    #                 return self.tiles[j][i]
    #     return None

    # def get_enemy_tiles(self) -> list[Tile]:
    #     tiles = []
    #     for i in range(self.tile_count_y - 1, -1, -1):
    #         for j in range(self.tile_count_x):
    #             if self.tiles[j][i].has_enemy:
    #                 tiles.append(self.tiles[j][i])
    #     return tiles
