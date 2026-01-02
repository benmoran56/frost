from pyglet.event import EVENT_HANDLED, EVENT_UNHANDLED

from .primitives import generate_frame
from .shaders import get_default_shader

import pyglet

from pyglet.enums import GeometryMode
from pyglet.graphics import ShaderGroup


class Frame:
    def __init__(self, window, title, x, y, width, border=3, spacer=8, group=None, batch=None):
        self._window = window
        self._x = x
        self._y = y
        self._trans_x = 0
        self._trans_y = 0
        self._width = width
        self._height = 0
        self._color1 = 25, 25, 25
        self._color2 = 50, 50, 50

        self._batch = batch or pyglet.graphics.Batch()
        self._program = get_default_shader()
        self._bgroup = ShaderGroup(self._program, order=0, parent=group)
        self._fgroup = ShaderGroup(self._program, order=1, parent=group)

        self._title = pyglet.text.Label(title, weight="bold", batch=self._batch, group=self._fgroup)
        self._title.x = x + 5
        self._title.y = y - self._title.content_height

        self._border = border
        self._menusize = self._title.content_height + 5
        self._widget_spacer = spacer

        self.in_drag = False

        self._widgets = []
        self._window.push_handlers(self)

        self._vertex_list = None
        self._update_vertex_list()

    def _update_vertex_list(self):
        self.delete()
        self._height = self._menusize + self._border * 2 + self._widget_stack_height
        self._height += self._widget_spacer if self._widget_stack_height else 0   # Don't add the spacer if no widgets
        verts, colors = generate_frame(x=self._x, y=self._y, width=self._width, height=self._height,
                                       border=self._border, menusize=self._menusize,
                                       color1=self._color1, color2=self._color2)
        count = len(verts) // 2
        self.vertex_list = self._program.vertex_list(count, GeometryMode.TRIANGLES,
                                                     self._batch, self._bgroup,
                                                     position=('f', verts),
                                                     colors=('Bn', colors),
                                                     translation=('f', (self._trans_x, self._trans_y) * count))

    @property
    def position(self):
        return self._x, self._y

    @property
    def _widget_stack_height(self):
        return sum([w.height + self._widget_spacer for w in self._widgets])

    def _get_new_widget_position(self, widget_height):
        """Automatically offset the position of the new widgets being added."""
        x = self._x + self._border + self._widget_spacer
        y = self._y - self._border - self._menusize - self._widget_spacer - widget_height - self._widget_stack_height
        return x, y

    def add_widget(self, widget):
        widget.batch = self._batch
        widget.group = self._fgroup
        widget.create_verts(*self._get_new_widget_position(widget.height))
        self._widgets.append(widget)
        self._update_vertex_list()

    def check_menu_hit(self, x, y):
        return (self._x < x < self._x + self._width and
                self._y - self._menusize - self._border < y < self._y)

    def check_body_hit(self, x, y):
        return (self._x < x < self._x + self._width and
                self._y - self._height + self._border < y < self._y - self._menusize - self._border)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_menu_hit(x, y):
            self.in_drag = True
            return EVENT_HANDLED

        if self.check_body_hit(x, y):
            for widget in self._widgets:
                widget.on_mouse_press(x, y, buttons, modifiers)
            return EVENT_HANDLED

        return EVENT_UNHANDLED

    def on_mouse_release(self, x, y, buttons, modifiers):
        self.in_drag = False
        for widget in self._widgets:
            widget.on_mouse_release(x, y, buttons, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.in_drag:
            # Update the menu title position:
            self._title.x += dx
            self._title.y += dy

            # Save the new position:
            self._x += dx
            self._y += dy
            self._trans_x += dx
            self._trans_y += dy

            # Update all widget, and frame translation:
            for widget in self._widgets:
                widget.update_verts(dx, dy)

            self.vertex_list.translation[:] = (self._trans_x, self._trans_y) * self.vertex_list.count

            return EVENT_HANDLED

        if self.check_body_hit(x, y):
            for widget in self._widgets:
                widget.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
            return EVENT_HANDLED

        return EVENT_UNHANDLED

    def on_mouse_scroll(self, x, y, mouse, direction):
        if self.check_body_hit(x, y):
            for widget in self._widgets:
                widget.on_mouse_scroll(x, y, mouse, direction)

    def draw(self):
        self._batch.draw()

    def delete(self):
        if hasattr(self, 'vertex_list'):
            self.vertex_list.delete()
        self._trans_x = self._trans_y = 0

    def __del__(self):
        self.delete()
