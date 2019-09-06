from pyglet.event import EventDispatcher
from pyglet.text import Label
from pyglet.gl import GL_TRIANGLES

from .primitives import *


class Widget(EventDispatcher):

    def __init__(self, width, height):
        self._x = 0
        self._y = 0
        self._width = width
        self._height = height

        self.batch = None
        self.group = None
        self._vertex_list = None
        self._label = None

        self._value = 0

    @property
    def height(self):
        return self._height

    @property
    def position(self):
        return self._x, self._y

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.dispatch_event('on_change', value)

    def create_verts(self, x, y):
        raise NotImplementedError

    def update_verts(self, dx, dy):
        self._x += dx
        self._y += dy
        if self._vertex_list:
            vertices = self._vertex_list.vertices[:]
            vertices[0::2] = [x + dx for x in vertices[0::2]]
            vertices[1::2] = [y + dy for y in vertices[1::2]]
            self._vertex_list.vertices[:] = vertices
        if self._label:
            self._label.x += dx
            self._label.y += dy

    def _check_hit(self, x, y):
        pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_release(self, x, y, buttons, modifiers):
        pass

    def __del__(self):
        if self._vertex_list:
            self._vertex_list.delete()
        if self._label:
            self._label.delete()

    def on_change(self, value):
        """Dispatched when value changes.

        :param value: value
        """


Widget.register_event_type('on_change')


class CheckBox(Widget):

    def __init__(self, name=""):
        super().__init__(width=16, height=16)
        self.name = name

    def create_verts(self, x, y):
        self.__del__()
        self._x = x
        self._y = y
        self._label = Label(self.name, x=x + self._width + 8, y=y+2,  batch=self.batch, group=self.group)
        verts, colors = checkbox(x=x, y=y, width=self._width, height=self._height, border=4, checked=self._value)
        self._vertex_list = self.batch.add(len(verts)//2, GL_TRIANGLES, self.group, ('v2f', verts), ('c3B', colors))

    def _check_hit(self, x, y):
        return self._x < x < self._x + self._width and self._y < y < self._y + self._height

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._check_hit(x, y):
            self._value = not self._value
            self.create_verts(*self.position)
            self.dispatch_event('on_change', self._value)
