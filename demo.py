import pyglet
import frost

# Create a Frame object, and attach it to a Window:
window = pyglet.window.Window()
frame = frost.Frame(window, "Title", x=100, y=350, width=200, border=3)


# Create a selection of Widgets:
checkbox1 = frost.CheckBox(name="Checky 1")
checkbox2 = frost.CheckBox(name="Checky 2")
anchored_label = frost.AnchoredLabel(text="Anchored Label")
slider = frost.Slider(value=50, name="slidey")
linked_label = frost.LinkedLabel(text="Slidey Value: ", widget=slider)
spacer = frost.Spacer()
pushbutton = frost.Button(width=32, name="Pushy")
linked_label2 = frost.LinkedLabel(text="Pushy Value: ", widget=pushbutton)

pending_widgets = [checkbox1, checkbox2, anchored_label, slider, linked_label, spacer, pushbutton, linked_label2]


@window.event
def on_key_press(*unused):
    if pending_widgets:
        frame.add_widget(pending_widgets.pop(0))


# Create some example event handlers for the Widgets:

@slider.event('on_change')
def my_on_change(value):
    print("Slider:", value)


@checkbox1.event
def on_change(value):
    print("Checkbox 1:", value)


@checkbox2.event
def on_change(value):
    print("Checkbox 2:", value)


@pushbutton.event
def on_change(value):
    print("Button: Pressed!" if value else "Button: Released!")


@window.event
def on_draw():
    window.clear()
    frame.draw()


if __name__ == "__main__":
    pyglet.app.run()
