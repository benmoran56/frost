import pyglet
import frost

window = pyglet.window.Window(width=960, height=540)
fps_display = pyglet.window.FPSDisplay(window)

frame = frost.Frame(window, "Title", x=30, y=20, width=200, height=300)

for i in range(3):
    checkbox = frost.CheckBox(name="Testing!!")
    frame.add_widget(checkbox)

    @checkbox.event
    def on_change(value):
        print("Changed!!", value)


@window.event
def on_draw():
    window.clear()
    frame.draw()
    fps_display.draw()


def update(dt):
    pass


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()
