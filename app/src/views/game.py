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

        self.game_objects = []
        self.board = Board(self.width, self.height, batch=self.batch)
        self.player = Player(board=self.board,
                             current_tile=self.board.tiles[0][0],
                             batch=self.batch)
        self.enemies = self.load_enemies(2, batch=self.batch)

        self.game_objects = [self.player] + self.enemies

        for obj in self.game_objects:
            for handler in obj.event_handlers:
                self.push_handlers(handler)
                self.event_stack_size += 1

    def load_enemies(self,
                     number_of_enemies: int,
                     batch: pyglet.graphics.Batch = None) -> list[Entity]:
        enemies = []
        for _ in range(number_of_enemies):
            offset = self.board.get_offset()
            x, y, = self.board.get_random_tile()
            new_enemy = Enemy(x + offset[0], y + offset[1],
                              batch=batch)
            enemies.append(new_enemy)
        return enemies

    def on_draw(self) -> None:
        self.clear()
        self.batch.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.player.handle_key_pressed(symbol)

    def update(self, delta_time: float) -> None:
        to_add = []

        for i in range(len(self.game_objects)):
            for j in range(i + 1, len(self.game_objects)):
                obj_1 = self.game_objects[i]
                obj_2 = self.game_objects[j]
                if not obj_1.dead and not obj_2.dead:
                    if obj_1.collides_with(obj_2):
                        obj_1.handle_collision_with(obj_2)
                        obj_2.handle_collision_with(obj_1)

        for object in self.game_objects:
            object.update(delta_time)
            to_add.extend(object.new_objects)
            object.new_objects = []

        for to_remove in [
                object for object in self.game_objects if object.dead
        ]:
            if to_remove == self.player:
                self.player.dead = True

            # Remove the object from any batches it is a member of
            to_remove.delete()

            # Remove the object from our list
            self.game_objects.remove(to_remove)

        # Add new objects to the list
        self.game_objects.extend(to_add)

        if self.player.dead:
            self.new_board()

    def run(self) -> None:
        pyglet.clock.schedule_interval(self.update, 1 / 120.0)
        pyglet.app.run()
