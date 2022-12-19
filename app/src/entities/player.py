from entities import Entity, Bullet
from resource_loader import player_image
from enums import Direction
import math


class Player(Entity):
    def __init__(self,
                 *args: str,
                 **kwargs: int) -> None:
        super().__init__(*args, img=player_image, **kwargs)
        self.direction: Direction = Direction.NORTH

    def update(self, delta_time: float) -> None:
        super(Player, self).update(delta_time)

    def fire(self) -> None:
        # Note: pyglet's rotation attributes are in "negative degrees"
        angle_radians = -math.radians(self.rotation - 90)

        # Create a new bullet just in front of the player
        new_bullet = Bullet(self.x, self.y, batch=self.batch)

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
