from pyglet.event import EventDispatcher
from pyglet.text import Label
from pyglet.gl import GL_TRIANGLES, GL_LINES

from .primitives import *


class Widget(EventDispatcher):

    _label = Label(" ")

    def __init__(self, width, height, name):
        self._x = 0
        self._y = 0
        self._width = width
        self._height = height
        self._name = name

        self.batch = None
        self.group = None
        self._vertex_list = None

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


Widget.register_event_type('on_change')


class Button(Widget):

    def __init__(self, name=""):
        super().__init__(width=16, height=16, name=name)

    def create_verts(self, x, y):
        self.__del__()
        self._x = x
        self._y = y
        self._label = Label(self._name, x=x + self._width + 8, y=y,  batch=self.batch, group=self.group, align='center')
        verts, colors = button(x=x, y=y, width=self._width, height=self._height, pressed=self._value)
        self._vertex_list = self.batch.add(len(verts)//2, GL_TRIANGLES, self.group, ('v2f', verts), ('c3B', colors))

    def _check_hit(self, x, y):
        return self._x < x < self._x + self._width and self._y < y < self._y + self._height

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._check_hit(x, y):
            self._value = True
            self.create_verts(self._x, self._y)
            self.dispatch_event('on_change', self._value)

    def on_mouse_release(self, x, y, buttons, modifiers):
        if self._value:
            self._value = False
            self.create_verts(self._x, self._y)


class CheckBox(Widget):

    def __init__(self, name=""):
        super().__init__(width=16, height=16, name=name)

    def create_verts(self, x, y):
        self.__del__()
        self._x = x
        self._y = y
        self._label = Label(self._name, x=x + self._width + 8, y=y+2,  batch=self.batch, group=self.group)
        verts, colors = checkbox(x=x, y=y, width=self._width, height=self._height, border=4, checked=self._value)
        self._vertex_list = self.batch.add(len(verts)//2, GL_TRIANGLES, self.group, ('v2f', verts), ('c3B', colors))

    def _check_hit(self, x, y):
        return self._x < x < self._x + self._width and self._y < y < self._y + self._height

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._check_hit(x, y):
            self._value = not self._value
            self.create_verts(*self.position)
            self.dispatch_event('on_change', self._value)


class Slider(Widget):

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
        self._vertex_list = self.batch.add(len(verts)//2, GL_TRIANGLES, self.group, ('v2f', verts), ('c3B', colors))

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


class TextEntry(Widget):

    def __init__(self, name=""):
        super().__init__(width=64, height=16, name=name)

    def create_verts(self, x, y):
        self.__del__()
        self._x = x
        self._y = y
        self._label = Label(self._name, x=x + self._width + 8, y=y+2,  batch=self.batch, group=self.group)
        verts, colors = textbox(x=x, y=y, width=self._width, height=self._height)
        self._vertex_list = self.batch.add(len(verts)//2, GL_LINES, self.group, ('v2f', verts), ('c3B', colors))


class AnchoredLabel(Widget):
    """Anchor point for pyglet label, handled through Frost"""
    def __init__(self, name="", text=""):
        super().__init__(width=1, height=16, name=name)
        self._text = text
        self._x = None
        self._y = None

    def create_verts(self, x, y):
        self.__del__()
        self._x = x
        self._y = y
        self._label = Label(self._text, x=x + self._width + 8, y=y+2,  batch=self.batch, group=self.group)
        # self._vertex_list = no vertices should be needed or used

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        if self._x:
            self.create_verts(self._x, self._y)


class LinkedLabel(AnchoredLabel):

    def __init__(self, name="", formatted_text="", obj=None, attrs=()):
        """where formatted_text is a string with a number of '%s' tokens equivalent to length of attrs
         attrs should be a tuple of string-ified attribute names for obj.
         these are str'd and then formatted into the label at the %s"""
        super().__init__(name=name, text="")
        self.obj = obj
        self.attrs = attrs
        self.ftext = formatted_text
        self._lastvals = None
        self._soft_update_text()

    def _soft_update_text(self):
        if self.obj:
            self._lastvals = tuple(getattr(self.obj, attr, "None") for attr in self.attrs)
            self.text = self.ftext % tuple(str(lv) for lv in self._lastvals)
        else:
            self.text = self.ftext % tuple(" " for i in range(self.ftext.count("%s")))

    def _scary_update_text(self):
        """only use if obj is known to exist"""
        lastvals = tuple(getattr(self.obj, attr, "None") for attr in self.attrs)
        if lastvals != self._lastvals:
            self._lastvals = lastvals
            self.text = self.text = self.ftext % tuple(str(lv) for lv in self._lastvals)

    def update(self, dt=0):
        if self.obj:
            self._scary_update_text()
