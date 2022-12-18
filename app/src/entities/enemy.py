from entities.entity import Entity
from enums import Direction
from resource_loader import player_image


class Enemy(Entity):
    def __init__(self, *args: str, **kwargs: int) -> None:
        super(Enemy, self).__init__(img=player_image, *args, **kwargs)
        self.direction: Direction = Direction.SOUTH

    def update(self, clock_interval: float) -> None:
        super(Enemy, self).update(clock_interval)
