from .primitives import *


class Widget:

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

        self._value = 0
        self.vertex_list = None

    def calculate_verts(self, x, y):
        raise NotImplementedError

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


class CheckBox(Widget):

    def __init__(self, x, y, width=16, height=16):
        super().__init__(x, y, width, height)

    def calculate_verts(self, x, y):
        return checkbox(x=x, y=y, width=self._width, height=self._height, border=4)

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
