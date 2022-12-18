from entities import Entity, Bullet
from resource_loader import player_image
from enums import Direction
import math
from collections import deque


[
    [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)],
    [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3)],
    [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)],
    [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)],
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
]

class Player(Entity):
    def __init__(self,
                 *args: str,
                 **kwargs: int) -> None:
        super().__init__(*args, img=player_image, **kwargs)
        self.direction: Direction = Direction.NORTH

    def update(self, delta_time: float) -> None:
        super(Player, self).update(delta_time)

    # def move(self) -> None:
    #     self.current_tile.has_player = False
    #     if self.direction == Direction.NORTH \
    #             and self.current_tile.y_index >= 1:
    #         self.current_tile = self.board \
    #             .tiles[self.current_tile.y_index - 1][self.current_tile.x_index]
    #         self.current_tile.has_player = True

    #     if self.direction == Direction.SOUTH \
    #             and self.current_tile.y_index <= self.board.tile_count_y - 2:
    #         self.current_tile = self.board \
    #             .tiles[self.current_tile.y_index + 1][self.current_tile.x_index]
    #         self.current_tile.has_player = True

    #     if self.direction == Direction.EAST \
    #             and self.current_tile.x_index >= 1:
    #         self.current_tile = self.board \
    #             .tiles[self.current_tile.y_index][self.current_tile.x_index - 1]
    #         self.current_tile.has_player = True

    #     if self.direction == Direction.WEST \
    #             and self.current_tile.x_index <= self.board.tile_count_x - 2:
    #         self.current_tile = self.board \
    #             .tiles[self.current_tile.y_index][self.current_tile.x_index + 1]
    #         self.current_tile.has_player = True

    #     self.x = self.current_tile.x + self.current_tile.width//2
    #     self.y = self.current_tile.y + self.current_tile.height//2

    def fire(self) -> None:
        # Note: pyglet's rotation attributes are in "negative degrees"
        angle_radians = -math.radians(self.rotation - 90)

        # Create a new bullet just in front of the player
        # ship_radius = self.image.width / 2
        bullet_x = self.x  # + math.cos(angle_radians) * ship_radius
        bullet_y = self.y  # + math.sin(angle_radians) * ship_radius
        new_bullet = Bullet(bullet_x, bullet_y, batch=self.batch)

        # Give it some speed
        bullet_vx = 0 + math.cos(angle_radians) * 200.0
        bullet_vy = 0 + math.sin(angle_radians) * 200.0
        new_bullet.velocity_x, new_bullet.velocity_y = bullet_vx, bullet_vy

        # Add it to the list of objects to be added to the game_objects list
        self.new_objects.append(new_bullet)

        # Play the bullet sound
        # resources.bullet_sound.play()

    def collides_with(self, other_object: Entity) -> bool:
        if isinstance(other_object, Bullet):
            return False
        return bool(super().collides_with(other_object))


    def bfs(self, matrix, start, queue, path, visited):
        # If the queue is empty, return None
        if not queue:
            return None

        # Set up the goal value (in this case, 1)
        goal = 1

        # Get the current position from the queue
        curr_pos = queue.popleft()

        # If the current position contains the goal value, return the path
        if matrix[curr_pos[0]][curr_pos[1]] == goal:
            return path

        # Mark the current position as visited
        visited.add(curr_pos)

        # Get the rows and columns of the matrix
        rows = len(matrix)
        cols = len(matrix[0])

        # Iterate over the adjacent positions
        for row_offset, col_offset in [(0,1), (0,-1), (1,0), (-1,0)]:
            # Calculate the new position
            new_row = curr_pos[0] + row_offset
            new_col = curr_pos[1] + col_offset

            # Check if the new position is valid (i.e., within the bounds of the matrix)
            # and has not been visited
            if 0 <= new_row < rows and 0 <= new_col < cols and (new_row, new_col) not in visited:
                # Add the new position to the queue and update the path dictionary
                queue.append((new_row, new_col))
                path[(new_row, new_col)] = curr_pos

        # Recursively call the function with the updated queue and path
        return bfs(matrix, start, queue, path, visited)

    def find_path(self, matrix, start):
        # Set up the queue, path dictionary, and visited set
        queue = deque([start])
        path = {start: None}
        visited = set()

        # Call the recursive function
        return bfs(matrix, start, queue, path, visited)
