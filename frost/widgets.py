from pyglet.event import EventDispatcher
from pyglet.text import Label
from pyglet.gl import GL_TRIANGLES

from .primitives import *


class Widget(EventDispatcher):

    def __init__(self, width, height, name):
        self._x = 0
        self._y = 0
        self._width = width
        self._height = height
        self._name = name

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

    def __init__(self, name="", minimum=0, maximum=100):
        super().__init__(width=64, height=16, name=name)
        self._min = minimum
        self._max = maximum

        self._knob_h = self._height
        self._knob_w = self._height // 2
        self._knob_x = 0

        self._in_update = False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.dispatch_event('on_change', value)

    # def _set_knob_position(self):
    #     self._knob_x = self._x  # TODO: value scaled
    #     self._knob_max = self._knob_x + self._width - self._knob_w
    #     # percent = ((self._value - self._min) * 100) / (self._max - self._min)

    def create_verts(self, x, y):
        self.__del__()
        self._x = x
        self._y = y
        self._knob_x = x
        self._label = Label(self._name, x=x + self._width + 8, y=y+2,  batch=self.batch, group=self.group)
        verts, colors = slider(x=x, y=y, width=self._width, height=self._height, bar=4, position=self._knob_x)
        self._vertex_list = self.batch.add(len(verts)//2, GL_TRIANGLES, self.group, ('v2f', verts), ('c3B', colors))

    def _check_hit(self, x, y):
        return self._x < x < self._x + self._width and self._y < y < self._y + self._height

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._check_hit(x, y):
            self._in_update = True

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._in_update:
            self._knob_x = max(self._x, min(x, self._x + self._width))
            self.create_verts(self._x, self._y)

    def on_mouse_release(self, x, y, buttons, modifiers):
        self._in_update = False
        # update value from knob position


class TextEntry(Widget):

    def __init__(self, name=""):
        super().__init__(width=64, height=16, name=name)

    def create_verts(self, x, y):
        self.__del__()
        self._x = x
        self._y = y
        self._label = Label(self._name, x=x + self._width + 8, y=y+2,  batch=self.batch, group=self.group)
        verts, colors = checkbox(x=x, y=y, width=self._width, height=self._height, border=4, checked=self._value)
        self._vertex_list = self.batch.add(len(verts)//2, GL_TRIANGLES, self.group, ('v2f', verts), ('c3B', colors))


class FrozenLabel(Widget):
    """Anchor point for pyglet label, handled through Frosty"""
    def __init__(self, name="", text=""):
        super().__init__(width=1, height=1, name=name)
        self.text = text
        self._x = None
        self._y = None

    def create_verts(self, x, y):
        self.__del__()
        self._x = x
        self._y = y
        self._label = Label(self.text, x=x + self._width + 8, y=y+2,  batch=self.batch, group=self.group)
        #self._vertex_list = no vertices should be needed or used

    @property
    def text(self):
        return self.text

    @text.setter
    def text(self, text):
        self.text = text
        if self._x:
            self.create_verts(self._x, self._y)


class LinkedLabel(FrozenLabel):

    def _update_text(self):
        if self.obj:
            self._lastvals = (getattr(self.obj, attr, "None") for attr in self.attrs)
            self.text = self.ftext % str(self._lastvals)
        else:
            self.text = self.ftext % (" " for i in range(self.ftext.count("%s")))

    def _scary_update_text(self):
        """only use if obj is known to exist"""
        self._lastvals = (getattr(self.obj, attr, "None") for attr in self.attrs)
        self.text = self.ftext % str(self._lastvals)

    def __init__(self, name="", formatted_text="", obj=None, attrs=()):
        """where formatted_text is a string with a number of '%s' tokens equivalent to length of attrs
         attrs should be a tuple of string-ified attribute names for obj.
         these are str'd and then formatted into the label at the %s"""
        super().__init__(name=name, text=formatted_text)
        self.obj = obj
        self.attrs = attrs
        self.ftext = formatted_text
        self._lastvals = None

    def update(self, dt):
        if self.obj:
            vals = getattr(self.obj, self.attrs, "None")
            if vals != self._lastvals:
                self._scary_update_text()