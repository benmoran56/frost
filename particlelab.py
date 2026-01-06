import frost
import pyglet

from pyglet.experimental import particles


window = pyglet.window.Window(1280, 720)
batch = pyglet.graphics.Batch()
# TODO: use same batch
frame = frost.Frame("Particle Settings", x=25, y=window.height - 25, border=6)

active_emmitters = []

img = pyglet.image.SolidColorImagePattern(color=(255, 255, 255, 255)).create_image(5, 5)
# img = pyglet.resource.texture('pyglet.png')
partical_man = particles.ParticleManager(img, lifespan=10, count=5,
                                         velocity=(30, 30), spread=(1.0, 1.0),
                                         color_start=(200, 0, 0, 200), color_end=(255, 255, 0, 50),
                                         scale_start=(1.0, 1.0), scale_end=(0.5, 0.5),
                                         batch=batch)

clear = frost.Button(width=32, name='clear all')
count = frost.Slider(width=100, value=partical_man.count, maximum=50, name='count')
count_label = frost.LinkedLabel(widget=count)
velocity_x = frost.Slider(width=150, value=partical_man.velocity[0])
velocity_x_label = frost.LinkedLabel("velocity x: ", widget=velocity_x)
velocity_y = frost.Slider(width=150, value=partical_man.velocity[1])
velocity_y_label = frost.LinkedLabel("velocity y: ", widget=velocity_y)
_r, _g, _b, _a = partical_man.color_start
rgb_r = frost.Slider(value=_r, width=100, maximum=255, name="Start RED")
rgb_g = frost.Slider(value=_g, width=100, maximum=255, name="Start GREEN")
rgb_b = frost.Slider(value=_b, width=100, maximum=255, name="Start BLUE")
rgb_a = frost.Slider(value=_a, width=100, maximum=255, name="Start ALPHA")
_r, _g, _b, _a = partical_man.color_end
rgb_r_e = frost.Slider(value=_r, width=100, maximum=255, name="End RED")
rgb_g_e = frost.Slider(value=_g, width=100, maximum=255, name="End GREEN")
rgb_b_e = frost.Slider(value=_b, width=100, maximum=255, name="End BLUE")
rgb_a_e = frost.Slider(value=_a, width=100, maximum=255, name="End ALPHA")
scale_start_x = frost.Slider(value=partical_man.scale_start[0], maximum=10, name='start scale x')
scale_start_y = frost.Slider(value=partical_man.scale_start[1], maximum=10, name='start scale y')
scale_end_x = frost.Slider(value=partical_man.scale_end[0], maximum=10, name='end scale x')
scale_end_y = frost.Slider(value=partical_man.scale_end[1], maximum=10, name='end scale y')

frame.add_widget(clear)
frame.add_widget(frost.Spacer())
frame.add_widget(count)
frame.add_widget(count_label)
frame.add_widget(velocity_x)
frame.add_widget(velocity_x_label)
frame.add_widget(velocity_y)
frame.add_widget(velocity_y_label)
frame.add_widget(frost.Spacer(height=8))
frame.add_widget(frost.AnchoredLabel("-- start/end colors --"))
frame.add_widget(rgb_r)
frame.add_widget(rgb_g)
frame.add_widget(rgb_b)
frame.add_widget(rgb_a)
frame.add_widget(frost.Spacer(height=4))
frame.add_widget(rgb_r_e)
frame.add_widget(rgb_g_e)
frame.add_widget(rgb_b_e)
frame.add_widget(rgb_a_e)
frame.add_widget(frost.Spacer(height=8))
frame.add_widget(frost.AnchoredLabel("-- Start/End scaling --"))
frame.add_widget(scale_start_x)
frame.add_widget(scale_start_y)
frame.add_widget(scale_end_x)
frame.add_widget(scale_end_y)


print(frame._width)
print()


for widget in frame._widgets:
    print(widget._name, widget.width)

@count.event
def on_change(value):
    partical_man.count = int(value)


@velocity_x.event
def on_change(value):
    partical_man.velocity = value, partical_man.velocity[1]


@velocity_y.event
def on_change(value):
    partical_man.velocity = partical_man.velocity[0], value

##############################

@rgb_r.event
def on_change(value):
    r, g, b, a = partical_man.color_start
    partical_man.color_start = int(value), g, b, a


@rgb_g.event
def on_change(value):
    r, g, b, a = partical_man.color_start
    partical_man.color_start = r, int(value), b, a

@rgb_b.event
def on_change(value):
    r, g, b, a = partical_man.color_start
    partical_man.color_start = r, g, int(value), a

@rgb_a.event
def on_change(value):
    r, g, b, a = partical_man.color_start
    partical_man.color_start = r, g, b, int(value)


@rgb_r_e.event
def on_change(value):
    r, g, b, a = partical_man.color_end
    partical_man.color_end = int(value), g, b, a

@rgb_g_e.event
def on_change(value):
    r, g, b, a = partical_man.color_end
    partical_man.color_end = r, int(value), b, a

@rgb_b_e.event
def on_change(value):
    r, g, b, a = partical_man.color_end
    partical_man.color_end = r, g, int(value), a

@rgb_a_e.event
def on_change(value):
    r, g, b, a = partical_man.color_end
    partical_man.color_end = r, g, b, int(value)

######################################

@scale_start_x.event
def on_change(value):
    partical_man.scale_start = value, partical_man.scale_start[1]


@scale_start_y.event
def on_change(value):
    partical_man.scale_start = partical_man.scale_start[0], value

@scale_end_x.event
def on_change(value):
    partical_man.scale_end = value, partical_man.scale_end[1]


@scale_end_y.event
def on_change(value):
    partical_man.scale_end = partical_man.scale_end[0], value


#################################

@clear.event
def on_change(value):
    for emitter in active_emmitters:
        emitter.delete()
    active_emmitters.clear()


################################

@window.event
def on_mouse_press(x, y, button, modifiers):
    emmitter = partical_man.create_emitter(x, y)
    active_emmitters.append(emmitter)


@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    emmitter = partical_man.create_emitter(x, y)
    active_emmitters.append(emmitter)


def update(dt):
    window.clear()
    batch.draw()
    frame.draw()


window.push_handlers(frame)

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
