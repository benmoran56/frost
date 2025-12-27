from .primitives import generate_frame
from .shaders import get_default_shader

import pyglet


from pyglet.graphics import GeometryMode, ShaderGroup



class Frame:
    def __init__(self, window, title, x, y, width, height, border=3, group=None, batch=None):
        self._window = window
        self._x = x
        self._y = y
        self._width = width
        self._height = height

        self._border = border
        self._menusize = 24
        self._widget_buffer = 8

        self._color1 = 25, 25, 25
        self._color2 = 50, 50, 50

        self._batch = batch or pyglet.graphics.Batch()
        self._program = get_default_shader()
        self._bgroup = ShaderGroup(self._program, order=0, parent=group)
        self._fgroup = ShaderGroup(self._program, order=1, parent=group)

        self._title = pyglet.text.Label(title, weight="bold", batch=self._batch, group=self._fgroup)
        self._title.x = x + 5
        self._title.y = y + height - self._title.content_height

        self.in_update = False

        self._widgets = []
        self._window.push_handlers(self)

        self._create_vertex_list()

    def _create_vertex_list(self):

        # TODO: anchor from top-left

        verts, colors = generate_frame(x=self._x, y=self._y, width=self._width, height=self._height,
                                       border=self._border, menusize=self._menusize,
                                       color1=self._color1, color2=self._color2)
        self.vertex_list = self._program.vertex_list(len(verts) // 2, GeometryMode.TRIANGLES,
                                                     self._batch, self._bgroup,
                                                     vertices=('f', verts), colors=('Bn', colors))

    @property
    def position(self):
        return self._x, self._y

    def _get_widget_position(self, widget_height):
        """Automatically offset the position of the new widgets being added."""
        existing = sum([w.height + self._widget_buffer for w in self._widgets])
        x = self._x + self._border + self._widget_buffer
        y = self._y + self._height - self._border - self._menusize - self._widget_buffer - existing - widget_height
        return x, y

    def add_widget(self, widget):
        self._window.push_handlers(widget)
        widget.batch = self._batch
        widget.group = self._fgroup
        widget.create_verts(*self._get_widget_position(widget.height))
        self._widgets.append(widget)

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

        # Update all widget, and frame positions:
        for widget in self._widgets:
            widget.update_verts(dx, dy)

        vertices = self.vertex_list.vertices[:]
        vertices[0::2] = [x + dx for x in vertices[0::2]]
        vertices[1::2] = [y + dy for y in vertices[1::2]]
        self.vertex_list.vertices[:] = vertices

        # Update the menu title position:
        self._title.x += dx
        self._title.y += dy

        # Save the new position:
        self._x += dx
        self._y += dy

    def draw(self):
        self._batch.draw()

    def delete(self):
        if getattr(self, 'vertex_list'):
            self.vertex_list.delete()

    def __del__(self):
        self.delete()
