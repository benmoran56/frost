from pyglet.gl import GL_TRIANGLES
from pyglet.text import Label
from pyglet.event import EventDispatcher

from .primitives import *
from .shaders import get_default_shader, FrostGroup


class _Widget(EventDispatcher):

    _label = Label(" ")

    def __init__(self, width, height, name=""):
        self._x = 0
        self._y = 0
        self._width = width
        self._height = height
        self._name = name

        self.batch = None
        self._program = get_default_shader()
        self._group = FrostGroup(program=self._program)
        self._vertex_list = None

        self._value = 0

    @property
    def group(self):
        return self._group.parent

    @group.setter
    def group(self, group):
        if self._group.parent == group:
            return
        self._group = FrostGroup(self._program, parent=group)
        # self.batch.migrate(self._vertex_list, GL_TRIANGLES, self._group, self.batch)

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
        self.create_verts(self._x, self._y)
        self.dispatch_event('on_change', value)

    def create_verts(self, x, y):
        raise NotImplementedError

    def update_verts(self, dx, dy):
        """Call with delta x/y to move existing vertices."""
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


_Widget.register_event_type('on_change')


class Button(_Widget):

    def __init__(self, name=""):
        super().__init__(width=16, height=16, name=name)

    def create_verts(self, x, y):
        self.__del__()
        self._x = x
        self._y = y
        self._label = Label(self._name, x=x + self._width + 8, y=y,  batch=self.batch, group=self.group, align='center')
        verts, colors = button(x=x, y=y, width=self._width, height=self._height, pressed=self._value)
        self._vertex_list = self._program.vertex_list(len(verts)//2, GL_TRIANGLES,
                                                      self.batch, self._group,
                                                      vertices=('f', verts), colors=('Bn', colors))

    def _check_hit(self, x, y):
        return self._x < x < self._x + self._width and self._y < y < self._y + self._height

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._check_hit(x, y):
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
        self.__del__()
        self._x = x
        self._y = y
        self._label = Label(self._name, x=x + self._width + 8, y=y+2,  batch=self.batch, group=self.group)
        verts, colors = checkbox(x=x, y=y, width=self._width, height=self._height, border=4, checked=self._value)

        self._vertex_list = self._program.vertex_list(len(verts)//2, GL_TRIANGLES, self.batch, self._group,
                                                      vertices=('f', verts), colors=('Bn', colors))

    def _check_hit(self, x, y):
        return self._x < x < self._x + self._width and self._y < y < self._y + self._height

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._check_hit(x, y):
            self._value = not self._value
            self.create_verts(*self.position)
            self.dispatch_event('on_change', self._value)


class Slider(_Widget):

    def __init__(self, name=""):
        super().__init__(width=64, height=16, name=name)
        self._knob_h = self._height
        self._knob_w = self._height // 4
        self._knob_x = 0
        self._in_update = False

    def create_verts(self, x, y):
        self.__del__()
        self._x = x
        self._y = y
        self._knob_x = self._knob_x or x
        self._label = Label(self._name, x=x + self._width + 8, y=y+2,  batch=self.batch, group=self.group)
        verts, colors = slider(x=x, y=y, width=self._width, height=self._height, bar=4, position=self._knob_x - self._knob_w)

        self._vertex_list = self._program.vertex_list(len(verts)//2, GL_TRIANGLES, self.batch, self._group,
                                                      vertices=('f', verts), colors=('Bn', colors))

    def _check_hit(self, x, y):
        return self._x < x < self._x + self._width and self._y < y < self._y + self._height

    def _update_knob(self, x):
        self._knob_x = max(self._x, min(x, self._x + self._width))
        self.value = abs(((self._knob_x - self._x) * 100) / (self._x - self._width - self._x))

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._check_hit(x, y):
            self._in_update = True
            self._update_knob(x)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._in_update:
            self._update_knob(x)

    def on_mouse_scroll(self, x, y, mouse, direction):
        if self._check_hit(x, y):
            self._update_knob(self._knob_x + direction/4)

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
        self.__del__()
        self._x = x
        self._y = y
        self._label = Label(self._text, x=x + self._width + 8, y=y+2,  batch=self.batch, group=self.group)
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
        super().__init__(text=f"{text} {widget.value}")

    def _update(self, value):
        self.text = f"{self._label_text} {value}"
