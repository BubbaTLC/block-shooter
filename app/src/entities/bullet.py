import pyglet
from entities.entity import Entity
from resource_loader import bullet_image


class Bullet(Entity):
    def __init__(self, *args, **kwargs):
        super(Bullet, self).__init__(bullet_image, *args, **kwargs)
        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.speed = 200

        # Bullets shouldn't stick around forever
        pyglet.clock.schedule_once(self.die, 2)

    def update(self, delta_interval: float) -> None:
        self.x += self.velocity_x * delta_interval
        self.y += self.velocity_y * delta_interval

    def die(self, delta_time: float):
        self.dead = True
