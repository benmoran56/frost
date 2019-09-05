from pyglet.event import EventDispatcher

from .primitives import *


class Widget(EventDispatcher):

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

        self.vertex_list = None

        self._value = 0

    @property
    def position(self):
        return self._x, self._y

    @position.setter
    def position(self, value):
        self._x, self._y = value
        if self.vertex_list:
            vertices = self.vertex_list.vertices[:]
            vertices[0::2] = [x + value[0] for x in vertices[0::2]]
            vertices[1::2] = [y + value[1] for y in vertices[1::2]]

    def calculate_verts(self, x, y):
        raise NotImplementedError

    def _check_hit(self, x, y):
        return (self._x < x < self._x + self._width and
                self._y + self._height < y < self._y + self._height)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._check_hit(x, y):
            pass

    def on_mouse_release(self, x, y, buttons, modifiers):
        pass

    def __del__(self):
        if self.vertex_list:
            self.vertex_list.delete()

    def on_change(self, value):
        """Dispatched when value changes.

        :param value: value
        """


Widget.register_event_type('on_change')


class CheckBox(Widget):

    def __init__(self, x, y, width=16, height=16):
        super().__init__(x, y, width, height)

    def calculate_verts(self, x, y):
        self._x = x
        self._y = y
        return checkbox(x=x, y=y, width=self._width, height=self._height, border=4, checked=self._value)

    def _check_hit(self, x, y):
        return (self._x < x < self._x + self._width and
                self._y + self._height < y < self._y + self._height)

    def on_mouse_press(self, x, y, buttons, modifiers):
        print(x, y)
        if self._check_hit(x, y):
            self._value = not self._value
            self.dispatch_event('on_change', self._value)

    def on_mouse_release(self, x, y, buttons, modifiers):
        pass

    def __del__(self):
        if self.vertex_list:
            self.vertex_list.delete()

