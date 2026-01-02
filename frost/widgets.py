from pyglet.enums import GeometryMode
from pyglet.graphics import ShaderGroup
from pyglet.text import Label
from pyglet.event import EventDispatcher
from pyglet.math import clamp

from .primitives import *
from .shaders import get_default_shader


class _Widget(EventDispatcher):

    def __init__(self, width=16, height=16, name=""):
        self._x = 0
        self._y = 0
        self._width = width
        self._height = height
        self._name = name
        self._value = 0

        self.batch = None
        self._program = get_default_shader()
        self._group = ShaderGroup(program=self._program)
        self._vertex_list = None
        self._label = None

    @property
    def group(self):
        return self._group.parent

    @group.setter
    def group(self, group):
        if self._group.parent == group:
            return
        self._group = ShaderGroup(self._program, parent=group)

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
        self.delete()
        self.create_verts(self._x, self._y)
        self.dispatch_event('on_change', self._value)

    def create_verts(self, x, y):
        raise NotImplementedError

    def update_verts(self, dx, dy):
        """Call with delta x/y to move existing vertices."""
        self._x += dx
        self._y += dy
        if self._vertex_list:
            position = self._vertex_list.position[:]
            position[0::2] = [x + dx for x in position[0::2]]
            position[1::2] = [y + dy for y in position[1::2]]
            self._vertex_list.position[:] = position
        if self._label:
            self._label.x += dx
            self._label.y += dy

    def check_hit(self, x, y):
        return self._x < x < self._x + self._width and self._y < y < self._y + self._height

    def delete(self):
        if self._vertex_list:
            self._vertex_list.delete()
            self._vertex_list = None
        if self._label:
            self._label.delete()
            self._label = None

    def __del__(self):
        self.delete()

    # Handlers

    def on_mouse_press(self, x, y, buttons, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_release(self, x, y, buttons, modifiers):
        pass

    # Events

    def on_change(self, value):
        """Dispatched when value changes.

        :param value: value
        """


_Widget.register_event_type('on_change')


class Button(_Widget):

    def __init__(self, name=""):
        super().__init__(width=16, height=16, name=name)

    def create_verts(self, x, y):
        self.delete()
        self._x = x
        self._y = y
        self._label = Label(self._name, x=x + self._width + 8, y=y,  batch=self.batch, group=self.group, align='center')
        verts, colors = button(x=x, y=y, width=self._width, height=self._height, pressed=self._value)
        self._vertex_list = self._program.vertex_list(len(verts)//2, GeometryMode.TRIANGLES,
                                                      self.batch, self._group,
                                                      position=('f', verts), colors=('Bn', colors))

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_hit(x, y):
            self._value = True
            self.create_verts(self._x, self._y)
            self.dispatch_event('on_change', True)

    def on_mouse_release(self, x, y, buttons, modifiers):
        if self._value:
            self._value = False
            self.create_verts(self._x, self._y)
            self.dispatch_event('on_change', False)


class CheckBox(_Widget):

    def __init__(self, name=""):
        super().__init__(width=16, height=16, name=name)

    def create_verts(self, x, y):
        self.delete()
        self._x = x
        self._y = y
        self._label = Label(self._name, x=x + self._width + 8, y=y+2,  batch=self.batch, group=self.group)
        verts, colors = checkbox(x=x, y=y, width=self._width, height=self._height, border=4, checked=self._value)

        self._vertex_list = self._program.vertex_list(len(verts)//2, GeometryMode.TRIANGLES, self.batch, self._group,
                                                      position=('f', verts), colors=('Bn', colors))

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_hit(x, y):
            self._value = not self._value
            self.create_verts(*self.position)
            self.dispatch_event('on_change', self._value)


class Slider(_Widget):

    def __init__(self, width=64, height=16, name=""):
        super().__init__(width=width, height=height, name=name)
        self._knob_h = self._height
        self._knob_w = self._height // 4
        self._knob_x = 0
        self._in_update = False

    def create_verts(self, x, y):
        self.delete()
        self._x = x
        self._y = y
        self._value = clamp(self._value, 0, 100)
        # Calculate the x position from the value:
        self._knob_x = (self._value * (x + self._width - x)) / 100 + x
        self._label = Label(self._name, x=x + self._width + 8, y=y+2,  batch=self.batch, group=self.group)
        verts, colors = slider(x=x, y=y, width=self._width, height=self._height, bar=4, position=self._knob_x - self._knob_w)

        self._vertex_list = self._program.vertex_list(len(verts)//2, GeometryMode.TRIANGLES, self.batch, self._group,
                                                      position=('f', verts), colors=('Bn', colors))

    def _x_to_percentage(self, x):
        x1 = self._x
        x2 = self._x + self._width
        return round(((x - x1) / (x2 - x1)) * 100, 2)

    def _percent_to_x(self, percentage):
        x1 = self._x
        x2 = self._x + self._width
        return (percentage * (x2 - x1)) / 100 + x1

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_hit(x, y):
            self._in_update = True
            self.value = self._x_to_percentage(x)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._in_update:
            self.value = self._x_to_percentage(x)

    def on_mouse_scroll(self, x, y, mouse, direction):
        if self.check_hit(x, y):
            self.value = self.value + direction

    def on_mouse_release(self, x, y, buttons, modifiers):
        self._in_update = False


class AnchoredLabel(_Widget):
    """Anchor point for pyglet label, handled through Frost"""
    def __init__(self, text=""):
        super().__init__(width=1, height=16)
        self._text = text
        self._x = None
        self._y = None

    def create_verts(self, x, y):
        self.delete()
        self._x = x
        self._y = y
        self._label = Label(self._text, x=x + self._width, y=y+2,  batch=self.batch, group=self.group)
        # self._vertex_list = no additional vertices are needed

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        if self._x:
            self.create_verts(self._x, self._y)


class LinkedLabel(AnchoredLabel):

    def __init__(self, text="", widget=None):
        """Automatically updating Label

        LinkedLabels are automatically updated when the
        attached Widget's value changes.
        """
        self._label_text = text
        self._widget = widget
        self._widget.on_change = self._update
        super().__init__(text=f"{text}{widget.value}")

    def _update(self, value):
        self.text = f"{self._label_text}{value}"


class Spacer(_Widget):

    def create_verts(self, x, y):
        """Just a spacer - no need to create anything."""
