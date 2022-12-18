from collections import deque
import pyglet
from pyglet.window import key
from enums import Direction
from entities import Player, Enemy, Entity


def get_invert_matrix(x: int, y: int, matrix: list[list]) -> tuple:
    return tuple(matrix[len(matrix) - y - 1][x])


class Tile(pyglet.shapes.Rectangle):
    def __init__(self,
                 vector: tuple,
                 player: Player = None,
                 enemy: Enemy = None,
                 *args: str,
                 **kwargs: int):
        super(Tile, self).__init__(*args, **kwargs)
        self.color = (58, 58, 58)
        self.vector = vector
        self.x_index = vector[0]
        self.y_index = vector[1]
        self.enemy = enemy
        self.player = player


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
        self.create_tiles()
        self.player: Player = self.place_player()
        self.enemies: list[Enemy] = self.place_enemies()
        self.event_handlers: list = []

    def handle_key_pressed(self, symbol: int) -> None:
        if symbol == key.LEFT:
            self.player.direction = Direction.WEST
        if symbol == key.RIGHT:
            self.player.direction = Direction.EAST
        if symbol == key.UP:
            self.player.direction = Direction.NORTH
        if symbol == key.DOWN:
            self.player.direction = Direction.SOUTH

        self.player.rotation = self.player.direction.value

        if symbol == key.SPACE:
            self.move()

    def get_2d_matrix(self, rows: int, columns: int) -> list[list]:
        return [
            [(i, j) for i in range(columns)]
            for j in range(rows - 1, -1, -1)
        ]

    def get_tile(self, x: int, y: int) -> Tile:
        return self.tiles[self.tile_count_y - y - 1][x]

    def get_tile_positions(self, x: int, y: int) -> tuple:
        return self.tile_positions[self.tile_count_y - y - 1][x]

    def create_tiles(self) -> None:
        total_padding_x = self.padding * (self.tile_count_x + 1)
        total_padding_y = self.padding * (self.tile_count_y + 1)
        available_width = self.width - total_padding_x
        available_height = self.height - total_padding_y
        self.tile_width = int(available_width / self.tile_count_x)
        self.tile_height = int(available_height / self.tile_count_y)

        for i in range(self.tile_count_y - 1, -1, -1):
            for j in range(self.tile_count_x):
                x = j * self.tile_width + (j + 1) * self.padding
                y = ((self.tile_count_y - 1 - i) * self.tile_height) + \
                    ((self.tile_count_y - 1 - i + 1) * self.padding)
                self.tiles[i][j] = Tile(x=x,
                                        y=y,
                                        vector=self.tile_positions[i][j],
                                        height=self.tile_height,
                                        width=self.tile_width,
                                        batch=self.batch)

    def place_player(self) -> Player:
        tile = self.get_tile(0, 1)
        x = tile.x + self.tile_width//2
        y = tile.y + self.tile_height//2
        player = Player(x=x,
                        y=y,
                        batch=self.batch)
        tile.player = player
        return player

    def place_enemies(self) -> list[Enemy]:
        tile = self.get_tile(0, 4)
        x = tile.x + self.tile_width//2
        y = tile.y + self.tile_height//2
        enemy = Enemy(x=x,
                      y=y,
                      batch=self.batch)
        tile.enemy = enemy
        return [enemy]

    def update(self, delta_time: float) -> None:
        pass

    def get_offset(self) -> tuple:
        return (self.tile_width//2, self.tile_height//2)

    def get_size(self) -> tuple:
        return (self.width, self.height)

    def get_player_tile(self) -> Tile:
        for i in range(self.tile_count_y):
            for j in range(self.tile_count_x):
                if isinstance(self.tiles[i][j].player, Player):
                    return self.tiles[i][j]
        return None

    def get_enemy_tiles(self) -> list[Tile]:
        tiles = []
        for i in range(self.tile_count_y):
            for j in range(self.tile_count_x):
                if isinstance(self.tiles[i][j].enemy, Enemy):
                    tiles.append(self.tiles[i][j])
        return tiles

    def check_for_endgame(self) -> None:
        for tile in self.get_enemy_tiles():
            if tile == self.get_player_tile():
                self.player.dead = True

    def move(self) -> None:
        self.move_player()
        self.move_enemy()

        self.check_for_endgame()

    def move_player(self) -> None:
        current_tile = self.get_player_tile()
        new_tile = current_tile
        print("current", current_tile.vector)
        if self.player.direction == Direction.NORTH \
                and current_tile.y_index >= 1:
            new_tile = self.get_tile(current_tile.x_index,
                                     current_tile.y_index - 1)
            new_tile.player = self.player
            current_tile.player = None

        if self.player.direction == Direction.SOUTH \
                and current_tile.y_index <= self.tile_count_y - 2:
            new_tile = self.get_tile(current_tile.x_index,
                                     current_tile.y_index + 1)
            new_tile.player = self.player
            current_tile.player = None

        if self.player.direction == Direction.EAST \
                and current_tile.x_index >= 1:
            new_tile = self.get_tile(current_tile.x_index - 1,
                                     current_tile.y_index)
            new_tile.player = self.player
            current_tile.player = None

        if self.player.direction == Direction.WEST \
                and current_tile.x_index <= self.tile_count_x - 2:
            new_tile = self.get_tile(current_tile.x_index + 1,
                                     current_tile.y_index)
            new_tile.player = self.player
            current_tile.player = None

        print("new tile", new_tile.vector)
        self.player.x = new_tile.x + new_tile.width//2
        self.player.y = new_tile.y + new_tile.height//2

    def move_enemy(self) -> None:
        player_tile = self.get_player_tile()
        enemy_tiles = self.get_enemy_tiles()
        for enemy_tile in enemy_tiles:
            start = (enemy_tile.vector)
            path = self.find_path(self.tile_positions, start)
            shortest_path = []
            if path is not None:
                curr_pos = self.get_player_tile().vector
                while curr_pos != start:
                    shortest_path.append(curr_pos)
                    curr_pos = path[curr_pos]

                if shortest_path:
                    new_tile = self.get_tile(
                        shortest_path[len(shortest_path) - 0 - 1][0],
                        shortest_path[len(shortest_path) - 0 - 1][1]
                    )

                    enemy = enemy_tile.enemy
                    enemy.x = new_tile.x + new_tile.width//2
                    enemy.y = new_tile.y + new_tile.height//2
                    new_tile.enemy = enemy
                    enemy_tile.enemy = None

    def find_path(self, matrix: list[list], start: tuple) -> dict:
        queue = deque([start])
        path = {start: None}
        visited: set = set()
        return self.bfs(matrix, start, queue, path, visited)

    def bfs(self,
            matrix: list[list],
            start: tuple,
            queue: deque,
            path: dict,
            visited: set) -> dict:
        if not queue:
            return {}

        goal = self.get_player_tile().vector
        curr_pos = queue.popleft()

        if get_invert_matrix(curr_pos[0], curr_pos[1], matrix) == goal:
            return path

        visited.add(curr_pos)

        rows = len(matrix)
        cols = len(matrix[0])

        for row_offset, col_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row = curr_pos[0] + row_offset
            new_col = curr_pos[1] + col_offset

            if 0 <= new_row < rows and \
                0 <= new_col < cols and \
                    (new_row, new_col) not in visited:
                queue.append((new_row, new_col))
                path[(new_row, new_col)] = curr_pos

        return self.bfs(matrix, start, queue, path, visited)
