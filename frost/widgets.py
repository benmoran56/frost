from .primitives import *


class Widget:

    def __init__(self):
        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0
        self._value = 0

        self.vertex_list = None

    def check_hit(self, x, y):
        return (self._x < x < self._x + self._width and
                self._y + self._height < y < self._y + self._height)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_hit(x, y):
            pass

    def on_mouse_release(self, x, y, buttons, modifiers):
        pass

    def __del__(self):
        if self.vertex_list:
            self.vertex_list.delete()


class Button(Widget):
    pass
