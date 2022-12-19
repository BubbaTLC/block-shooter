from collections import deque
import random
import pyglet
from pyglet.window import key
from enums import Direction
from entities import Player, Enemy, Entity, Bullet


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
        self.tile_count_x: int = 10
        self.tile_count_y: int = 10
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
        self.game_objects = [self.player] + self.enemies
        self.event_handlers: list = []
        self.victory: bool = False

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
        tile = self.get_tile(4, 4)
        x = tile.x + self.tile_width//2
        y = tile.y + self.tile_height//2
        player = Player(x=x,
                        y=y,
                        vector=(4, 4),
                        batch=self.batch)
        tile.player = player
        return player

    def place_enemies(self) -> list[Enemy]:
        enemies = []
        for i in range(10):
            x_index, y_index = random.randint(0, 9), random.randint(0, 9)
            if (x_index, y_index) == (4, 4):
                continue
            tile = self.get_tile(x_index, y_index)
            x = tile.x + self.tile_width//2
            y = tile.y + self.tile_height//2
            enemy = Enemy(x=x,
                          y=y,
                          vector=(x_index, y_index),
                          batch=self.batch)
            tile.enemy = enemy
            enemies.append(enemy)
        return enemies

    def kill(self, entity: Entity) -> None:
        if isinstance(entity, Enemy):
            self.enemies.remove(entity)
            self.game_objects.remove(entity)
            for tile in self.get_enemy_tiles():
                if tile.enemy == entity:
                    tile.enemy = None
        if isinstance(entity, Bullet):
            self.game_objects.remove(entity)

    def get_offset(self) -> tuple:
        return (self.tile_width//2, self.tile_height//2)

    def get_size(self) -> tuple:
        return (self.width, self.height)

    def get_player_tile(self) -> Tile:
        return self.get_tile(self.player.x_index, self.player.y_index)

    def get_enemy_tiles(self) -> list[Tile]:
        tiles = []
        for enemy in self.enemies:
            tiles.append(self.get_tile(enemy.x_index, enemy.y_index))
        return tiles

    def check_for_endgame(self) -> None:
        tiles = self.get_enemy_tiles()
        for tile in tiles:
            if tile == self.get_player_tile():
                self.player.dead = True

        if not any(isinstance(obj, Enemy) for obj in self.game_objects):
            self.victory = True

    def move(self) -> None:
        self.player.fire()
        self.move_player()
        self.move_enemy()

    def move_player(self) -> None:
        current_tile = self.get_player_tile()
        new_tile = current_tile
        if self.player.direction == Direction.NORTH \
                and current_tile.y_index >= 1:
            new_tile = self.get_tile(current_tile.x_index,
                                     current_tile.y_index - 1)
            new_tile.player = self.player
            self.player.set_vector(new_tile.vector)
            current_tile.player = None

        if self.player.direction == Direction.SOUTH \
                and current_tile.y_index <= self.tile_count_y - 2:
            new_tile = self.get_tile(current_tile.x_index,
                                     current_tile.y_index + 1)
            new_tile.player = self.player
            self.player.set_vector(new_tile.vector)
            current_tile.player = None

        if self.player.direction == Direction.EAST \
                and current_tile.x_index >= 1:
            new_tile = self.get_tile(current_tile.x_index - 1,
                                     current_tile.y_index)
            new_tile.player = self.player
            self.player.set_vector(new_tile.vector)
            current_tile.player = None

        if self.player.direction == Direction.WEST \
                and current_tile.x_index <= self.tile_count_x - 2:
            new_tile = self.get_tile(current_tile.x_index + 1,
                                     current_tile.y_index)
            new_tile.player = self.player
            self.player.set_vector(new_tile.vector)
            current_tile.player = None

        self.player.x = new_tile.x + new_tile.width//2
        self.player.y = new_tile.y + new_tile.height//2

    def move_enemy(self) -> None:
        enemy_tiles = self.get_enemy_tiles()
        for enemy_tile in enemy_tiles:
            start = (enemy_tile.vector)
            path = self.find_path(self.tile_positions, start)
            shortest_path = []
            if path is None:
                return

            curr_pos = self.get_player_tile().vector
            while curr_pos != start:
                shortest_path.append(curr_pos)
                curr_pos = path[curr_pos]

            if not shortest_path:
                return
                
            new_tile = self.get_tile(
                shortest_path[len(shortest_path) - 0 - 1][0],
                shortest_path[len(shortest_path) - 0 - 1][1]
            )
            if not new_tile.enemy:
                enemy = enemy_tile.enemy
                enemy.x = new_tile.x + new_tile.width//2
                enemy.y = new_tile.y + new_tile.height//2
                enemy.set_vector(new_tile.vector)
                new_tile.enemy = enemy
                enemy_tile.enemy = None

    def find_path(self, matrix, start) -> dict:
        # Set up the queue, path dictionary, and visited set
        queue = deque([start])
        path = {start: None}
        visited = set()

        # Set up the goal value (in this case, 1)
        goal = self.get_player_tile().vector

        # Get the rows and columns of the matrix
        rows = len(matrix)
        cols = len(matrix[0])

        # Continue searching as long as there are items in the queue
        while queue:
            # Get the current position from the queue
            curr_pos = queue.popleft()

            # If the current position contains the goal value, return the path
            if get_invert_matrix(curr_pos[0], curr_pos[1], matrix) == goal:
                return path

            # Mark the current position as visited
            visited.add(curr_pos)

            # Iterate over the adjacent positions
            for row_offset, col_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                # Calculate the new position
                new_row = curr_pos[0] + row_offset
                new_col = curr_pos[1] + col_offset

                # Check if the new position is valid (i.e., within the bounds of the matrix)
                # and has not been visited
                if 0 <= new_row < rows \
                        and 0 <= new_col < cols \
                        and (new_row, new_col) not in visited:
                    # Add the new position to the queue and update the path dictionary
                    queue.append((new_row, new_col))
                    path[(new_row, new_col)] = curr_pos

        # If the queue is empty and the goal has not been found, return None
        return None

    # def find_path(self, matrix: list[list], start: tuple) -> dict:
    #     queue = deque([start])
    #     path = {start: None}
    #     visited: set = set()
    #     return self.bfs(matrix, start, queue, path, visited)

    # def bfs(self,
    #         matrix: list[list],
    #         start: tuple,
    #         queue: deque,
    #         path: dict,
    #         visited: set) -> dict:
    #     if not queue:
    #         return {}

    #     goal = self.get_player_tile().vector
    #     curr_pos = queue.popleft()

    #     if get_invert_matrix(curr_pos[0], curr_pos[1], matrix) == goal:
    #         return path

    #     visited.add(curr_pos)

    #     rows = len(matrix)
    #     cols = len(matrix[0])

    #     for row_offset, col_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    #         new_row = curr_pos[0] + row_offset
    #         new_col = curr_pos[1] + col_offset

    #         if 0 <= new_row < rows and \
    #             0 <= new_col < cols and \
    #                 (new_row, new_col) not in visited:
    #             queue.append((new_row, new_col))
    #             path[(new_row, new_col)] = curr_pos

    #     return self.bfs(matrix, start, queue, path, visited)
