from .primitives import simple_frame


import pyglet
from pyglet.gl import GL_TRIANGLES


class Frame:
    def __init__(self, window, title, x, y, width, height):
        self._window = window
        self._x = x
        self._y = y
        self._width = width
        self._height = height

        self._border = 3
        self._menusize = 25
        self._color1 = 25, 25, 25
        self._color2 = 50, 50, 50

        self._batch = pyglet.graphics.Batch()
        self._bgroup = pyglet.graphics.OrderedGroup(order=0)
        self._fgroup = pyglet.graphics.OrderedGroup(order=1)

        self._title = pyglet.text.Label(title, bold=True, batch=self._batch, group=self._fgroup)
        self._title.x = x + 5
        self._title.y = y + height - self._title.content_height

        verts, colors = simple_frame(x=x, y=y, width=width, height=height, border=self._border,
                                     menusize=self._menusize, color1=self._color1, color2=self._color2)
        self.vertex_list = self._batch.add(len(verts) // 2, GL_TRIANGLES, self._bgroup, ('v2f', verts), ('c3b', colors))
        self.in_update = False

        self._widgets = []
        self._window.push_handlers(self)

    @property
    def position(self):
        return self._x, self._y

    def _get_widget_position(self):
        return self._x + self._border + self._border, self._height - self._menusize

    def add_widget(self, widget):
        self._widgets.append(widget)
        self._window.push_handlers(widget)
        widget.batch = self._batch
        widget.group = self._fgroup
        widget.create_verts(*self._get_widget_position())

    def check_hit(self, x, y):
        return (self._x < x < self._x + self._width and
                self._y + self._height - self._menusize - self._border < y < self._y + self._height)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_hit(x, y):
            self.in_update = True

    def on_mouse_release(self, x, y, buttons, modifiers):
        self.in_update = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.in_update:
            return

        # Update the menu title position:
        self._title.x += dx
        self._title.y += dy

        # Update all widget, and frame positions:
        for widget in self._widgets:
            widget.update_verts(dx, dy)

        vertices = self.vertex_list.vertices[:]
        vertices[0::2] = [x + dx for x in vertices[0::2]]
        vertices[1::2] = [y + dy for y in vertices[1::2]]
        self.vertex_list.vertices[:] = vertices

        # Save the new position:
        self._x += dx
        self._y += dy

    def draw(self):
        self._batch.draw()
