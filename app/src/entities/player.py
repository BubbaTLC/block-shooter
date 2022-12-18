from pyglet.window import key
from views import Board, Tile
from entities import Entity, Bullet
from resource_loader import player_image
from enums import Direction
import math


class Player(Entity):
    def __init__(self,
                 *args: str,
                 current_tile: Tile,
                 board: Board,
                 **kwargs: int) -> None:
        super().__init__(*args, img=player_image, **kwargs)
        self.direction: Direction = Direction.NORTH
        self.board = board
        self.current_tile = current_tile
        self.x = self.current_tile.x + self.current_tile.width//2
        self.y = self.current_tile.y + self.current_tile.height//2

    def update(self, delta_time: float) -> None:
        super(Player, self).update(delta_time)

    def handle_key_pressed(self, symbol: int) -> None:
        if symbol == key.LEFT:
            self.direction = Direction.WEST
        if symbol == key.RIGHT:
            self.direction = Direction.EAST
        if symbol == key.UP:
            self.direction = Direction.NORTH
        if symbol == key.DOWN:
            self.direction = Direction.SOUTH

        if symbol == key.SPACE:
            self.fire()
            self.move()

        self.rotation = self.direction.value

    def move(self) -> None:
        if self.direction == Direction.NORTH \
                and self.current_tile.y_index >= 1:
            self.current_tile = self.board \
                .tiles[self.current_tile.y_index - 1][self.current_tile.x_index]

        if self.direction == Direction.SOUTH \
                and self.current_tile.y_index <= self.board.tile_count_y - 2:
            self.current_tile = self.board \
                .tiles[self.current_tile.y_index + 1][self.current_tile.x_index]

        if self.direction == Direction.EAST \
                and self.current_tile.x_index >= 1:
            self.current_tile = self.board \
                .tiles[self.current_tile.y_index][self.current_tile.x_index - 1] \

        if self.direction == Direction.WEST \
                and self.current_tile.x_index <= self.board.tile_count_x - 2:
            self.current_tile = self.board \
                .tiles[self.current_tile.y_index][self.current_tile.x_index + 1] \

        self.x = self.current_tile.x + self.current_tile.width//2
        self.y = self.current_tile.y + self.current_tile.height//2

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
