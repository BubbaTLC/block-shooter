import pyglet
from entities.entity import Entity


class Tile(pyglet.shapes.Rectangle):
    def __init__(self, *args: str, **kwargs: int):
        super(Tile, self).__init__(*args, **kwargs)
        # self.anchor_x = self.width / 2
        # self.anchor_y = self.height / 2
        self.color = (58, 58, 58)


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
        self.tile_positions: list[list[Tile]] = self.get_2d_matrix(
            self.tile_count_y, self.tile_count_x
        )
        self.tiles: list[list[Tile]] = []
        self.player_position: tuple = (self.width / 2, self.height / 2)
        self.load_tile_positions()
        self.create_tiles()

    def get_2d_matrix(self, rows: int, columns: int) -> list[list]:
        return [
            [None for _ in range(columns)]
            for _ in range(rows)
        ]

    def load_tile_positions(self):
        total_padding_x = self.padding * (self.tile_count_x + 1)
        total_padding_y = self.padding * (self.tile_count_y + 1)
        available_width = self.width - total_padding_x
        available_height = self.height - total_padding_y
        self.tile_width = available_width / self.tile_count_x
        self.tile_height = available_height / self.tile_count_y

        for i in range(self.tile_count_y):
            for j in range(self.tile_count_x):
                x = j * self.tile_width + (j + 1) * self.padding
                y = i * self.tile_height + (i + 1) * self.padding
                self.tile_positions[i][j] = (x, y)

    def create_tiles(self) -> None:
        for i in range(self.tile_count_y):
            for j in range(self.tile_count_x):
                x, y = self.tile_positions[i][j]
                self.tiles.append(Tile(x=x,
                                       y=y,
                                       height=self.tile_height,
                                       width=self.tile_width,
                                       batch=self.batch))

    def update(self) -> None:
        pass

