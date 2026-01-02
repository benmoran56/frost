import frost
import pyglet

from pyglet.experimental import particles


window = pyglet.window.Window(1280, 720)
batch = pyglet.graphics.Batch()
# TODO: use same batch
frame = frost.Frame("Particle Settings", x=25, y=window.height - 25, width=250, border=6)

active_emmitters = []

img = pyglet.image.SolidColorImagePattern(color=(255, 255, 255, 255)).create_image(5, 5)
# img = pyglet.resource.texture('pyglet.png')
partical_man = particles.ParticleManager(img, lifespan=10, count=5,
                                         velocity=(10, 10), spread=(1.0, 1.0),
                                         color_start=(200, 0, 0, 200), color_end=(255, 255, 0, 50),
                                         scale_start=(1.0, 1.0), scale_end=(0.5, 0.5),
                                         batch=batch)

checkbox1 = frost.CheckBox(name="update existing")
velocity_x = frost.Slider(width=150)
velocity_x_label = frost.LinkedLabel("velocity x: ", widget=velocity_x)
velocity_y = frost.Slider(width=150)
velocity_y_label = frost.LinkedLabel("velocity y: ", widget=velocity_y)
r, g, b, a = partical_man.color_start
rgb_r = frost.Slider(value=r, width=100, maximum=255, name="Start RED")
rgb_g = frost.Slider(value=g, width=100, maximum=255, name="Start GREEN")
rgb_b = frost.Slider(value=b, width=100, maximum=255, name="Start BLUE")
rgb_a = frost.Slider(value=a, width=100, maximum=255, name="Start ALPHA")
re, ge, be, ae = partical_man.color_end
rgb_r_e = frost.Slider(value=re, width=100, maximum=255, name="End RED")
rgb_g_e = frost.Slider(value=ge, width=100, maximum=255, name="End GREEN")
rgb_b_e = frost.Slider(value=be, width=100, maximum=255, name="End BLUE")
rgb_a_e = frost.Slider(value=ae, width=100, maximum=255, name="End ALPHA")
start_x, start_y = partical_man.scale_start
end_x, end_y = partical_man.scale_end
scale_start_x = frost.Slider(value=start_x, maximum=10, name='start scale x')
scale_start_y = frost.Slider(value=start_y, maximum=10, name='start scale y')
scale_end_x = frost.Slider(value=end_x, maximum=10, name='end scale x')
scale_end_y = frost.Slider(value=end_y, maximum=10, name='end scale y')

frame.add_widget(checkbox1)
frame.add_widget(frost.Spacer(height=8))
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

@velocity_x.event
def on_change(value):
    _, vely = partical_man.velocity
    partical_man.velocity = value, vely


@velocity_y.event
def on_change(value):
    velx, _ = partical_man.velocity
    partical_man.velocity = velx, value


@rgb_r.event
def on_change(value):
    global r
    r = int(value)
    partical_man.color_start = r, g, b, a


@rgb_g.event
def on_change(value):
    global g
    g = int(value)
    partical_man.color_start = r, g, b, a

@rgb_b.event
def on_change(value):
    global b
    b = int(value)
    partical_man.color_start = r, g, b, a

@rgb_a.event
def on_change(value):
    global a
    a = int(value)
    partical_man.color_start = r, g, b, a


@rgb_r_e.event
def on_change(value):
    global re
    re = int(value)
    partical_man.color_end = re, ge, be, ae

@rgb_g_e.event
def on_change(value):
    global ge
    ge = int(value)
    partical_man.color_end = re, ge, be, ae

@rgb_b_e.event
def on_change(value):
    global be
    be = int(value)
    partical_man.color_end = re, ge, be, ae

@rgb_a_e.event
def on_change(value):
    global ae
    ae = int(value)
    partical_man.color_end = re, ge, be, ae

######################################

@scale_start_x.event
def on_change(value):
    global start_x, start_y
    start_x = value
    partical_man.scale_start = start_x, start_y


@scale_start_y.event
def on_change(value):
    global start_x, start_y
    start_y = value
    partical_man.scale_start = start_x, start_y


@scale_end_x.event
def on_change(value):
    global end_x, end_y
    end_x = value
    partical_man.scale_end = end_x, end_y


@scale_end_y.event
def on_change(value):
    global end_x, end_y
    end_y = value
    partical_man.scale_end = end_x, end_y

################################

@window.event
def on_mouse_press(x, y, button, modifiers):
    partical_man.create_emitter(x, y)


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
