import pyglet
from pyglet.window import key

class MyWindow(pyglet.window.Window):

    def __init__(self):
        super(MyWindow, self).__init__()

        self.key_handler = key.KeyStateHandler()
        self.push_handlers(self.key_handler)

    def on_draw(self):
        self.clear()

    def update(self, _):
        if self.key_handler[key.UP]:
            print('UP key pressed')

if __name__ == '__main__':
    mygame = MyWindow()
    pyglet.clock.schedule_interval(mygame.update, 1/60)
    pyglet.app.run()