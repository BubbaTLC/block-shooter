import pyglet
from entities.entity import Entity
from resource_loader import bullet_image


class Bullet(Entity):
    def __init__(self, *args: str, **kwargs: int) -> None:
        super(Bullet, self).__init__(bullet_image, *args, **kwargs)
        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.speed = 200

        pyglet.clock.schedule_once(self.die, 3)

    def update(self, delta_interval: float) -> None:
        self.x += self.velocity_x * delta_interval
        self.y += self.velocity_y * delta_interval

    def die(self, delta_time: float) -> None:
        self.dead = True