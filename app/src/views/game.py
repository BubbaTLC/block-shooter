import pyglet
from pyglet.window import key
from entities import Entity, Player, Enemy
from views.board import Board


class Game(pyglet.window.Window):
    def __init__(self, *args: str, **kwargs: int) -> None:
        super(Game, self).__init__(*args, **kwargs)
        self.batch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.counter = pyglet.window.FPSDisplay(window=self)

        self.key_handler: key.KeyStateHandler = key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

        self.width = 500
        self.height = 500

        self.board: Board = None
        self.player: Player = None
        self.enemies: list[Enemy] = None
        self.score: int = 0
        self.game_objects: list[Entity] = []

        # We need to pop off as many event stack frames as we pushed on
        # every time we reset the level.
        self.event_stack_size: int = 0

        self.new_board()

    def new_board(self) -> None:
        while self.event_stack_size > 0:
            self.pop_handlers()
            self.event_stack_size -= 1

        self.board = Board(self.width, self.height, batch=self.batch)
        self.player = Player(x=self.width/2, y=self.height/2, batch=self.batch)
        self.enemies = self.load_enemies(2)

        self.game_objects = [self.player]

        for obj in self.game_objects:
            for handler in obj.event_handlers:
                self.push_handlers(handler)
                self.event_stack_size += 1

    def load_enemies(self,
                     number_of_enemies: int,
                     batch: pyglet.graphics.Batch = None) -> list[Entity]:
        return None

    def on_draw(self) -> None:
        self.clear()
        self.batch.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        self.player.handle_key_pressed(symbol)

    def update(self, delta_time: float) -> None:
        to_add = []

        for object in self.game_objects:
            object.update(delta_time)
            to_add.extend(object.new_objects)
            object.new_objects = []

        for to_remove in [object for object in self.game_objects if object.dead]:
            # If the dying object spawned any new objects, add those to the
            # game_objects list later
            # to_add.extend(to_remove.new_objects)

            # Remove the object from any batches it is a member of
            # to_remove.delete()

            # Remove the object from our list
            self.game_objects.remove(to_remove)

        # Add new objects to the list
        self.game_objects.extend(to_add)

    def run(self) -> None:
        pyglet.clock.schedule_interval(self.update, 1 / 120.0)
        pyglet.app.run()
