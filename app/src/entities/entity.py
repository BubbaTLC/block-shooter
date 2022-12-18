from __future__ import annotations
import pyglet
import math


class Entity(pyglet.sprite.Sprite):
    def __init__(self, *args: str, **kwargs: int) -> None:
        super(Entity, self).__init__(*args, **kwargs)
        # Flag to remove this object from the game_object list
        self.dead = False

        # List of new objects to go in the game_objects list
        self.new_objects: list[Entity] = []

        # Tell the game handler about any event handlers
        # Only applies to things with keyboard/mouse input

        self.tile_x_index = 0
        self.tile_y_index = 0

    def update(self, clock_interval: float) -> None:
        pass

    def collides_with(self, other_object: Entity) -> bool:
        # Calculate distance between object centers that would be a collision,
        # assuming square resources
        collision_distance: float = self.image.width * 0.5 * self.scale \
            + other_object.image.width \
            * 0.5 * other_object.scale

        # Get distance using position tuples
        actual_distance = self.distance(self.position, other_object.position)
        return actual_distance <= collision_distance

    def distance(self, point_1: tuple = (0, 0),
                 point_2: tuple = (0, 0)) -> float:
        """Returns the distance between two points"""
        return math.sqrt((point_1[0] - point_2[0]) ** 2 +
                         (point_1[1] - point_2[1]) ** 2)

    def handle_collision_with(self, other_object: None) -> None:
        # if not isinstance(other_object.__class__, self.__class__):
        if other_object.__class__ is not self.__class__:
            print("COLLISION")
            self.dead = True
