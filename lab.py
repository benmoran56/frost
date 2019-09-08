import pyglet
import frost

window = pyglet.window.Window(width=960, height=540)
frame = frost.Frame(window, "Title", x=30, y=20, width=200, height=300)

for i in range(2):
    checkbox = frost.CheckBox(name="Testing!!")
    frame.add_widget(checkbox)
    slider = frost.Slider(name="slidey")
    frame.add_widget(slider)

    @slider.event
    def on_change(value):
        print("Slider:", value)

    @checkbox.event
    def on_change(value):
        print("Checkbox:", value)


text_entry = frost.TextEntry("Input text")
frame.add_widget(text_entry)


@window.event
def on_draw():
    window.clear()
    frame.draw()


if __name__ == "__main__":
    pyglet.app.run()
