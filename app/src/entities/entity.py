import pyglet


class Entity(pyglet.sprite.Sprite):
    def __init__(self, *args: str, **kwargs: int) -> None:
        super(Entity, self).__init__(*args, **kwargs)
        # Flag to remove this object from the game_object list
        self.dead = False

        # List of new objects to go in the game_objects list
        self.new_objects: list[Entity] = []

        # Tell the game handler about any event handlers
        # Only applies to things with keyboard/mouse input
        self.event_handlers: list = []

    def update(self, clock_interval: float) -> None:
        pass

    def handle_collision_with(self, other_object: None) -> None:
        pass
