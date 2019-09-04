import pyglet
import frost

window = pyglet.window.Window(width=960, height=540)
batch = pyglet.graphics.Batch()

frame = frost.Frame(window, "Title", 30, 20, 200, 300, batch)
checkbox = frost.CheckBox(10, 10)

frame.add_widget(checkbox)


@window.event
def on_draw():
    window.clear()
    batch.draw()


if __name__ == "__main__":
    pyglet.app.run()
