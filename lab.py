import pyglet
import frost

window = pyglet.window.Window(width=960, height=540)
frame = frost.Frame(window, "Title", x=30, y=20, width=200, height=300)

checkbox = frost.CheckBox(name="Testing!!")
slider = frost.Slider(name="slidey")
text_entry = frost.TextEntry("Input text")
pushbutton = frost.Button("Pushy")
pushbutton2 = frost.Button("Pushy2")
lilabel = frost.LinkedLabel("label", "slidey value: %s", slider, ("value",))

frame.add_widget(checkbox)
frame.add_widget(slider)
frame.add_widget(text_entry)
frame.add_widget(pushbutton)
frame.add_widget(pushbutton2)
frame.add_widget(lilabel)


@slider.event
def on_change(value):
    print("Slider:", value)


@checkbox.event
def on_change(value):
    print("Checkbox:", value)


@pushbutton.event
def on_change(value):
    print("Button: Pressed!")


@window.event
def on_draw():
    window.clear()
    frame.draw()
    lilabel.update()


if __name__ == "__main__":
    pyglet.app.run()
