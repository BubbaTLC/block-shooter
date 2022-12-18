from entities.entity import Entity
from enums import Direction
from resource_loader import enemy_image


class Enemy(Entity):
    def __init__(self, *args: str, **kwargs: int) -> None:
        super(Enemy, self).__init__(enemy_image, *args, **kwargs)
        self.direction: Direction = Direction.SOUTH

    def update(self, clock_interval: float) -> None:
        super(Enemy, self).update(clock_interval)

    def handle_collision_with(self, other_object) -> None:
        super(Enemy, self).handle_collision_with(other_object)
