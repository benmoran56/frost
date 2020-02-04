import pyglet
import frost

# Create a Frame object, and attach it to a Window:
window = pyglet.window.Window(width=960, height=540)
frame = frost.Frame(window, "Title", x=30, y=20, width=200, height=300)


# Create a selection of Widgets:
checkbox1 = frost.CheckBox(name="Checky 1")
checkbox2 = frost.CheckBox(name="Checky 2")
anchored_label = frost.AnchoredLabel(text="-- Anchored Label --")
slider = frost.Slider(name="slidey")
linked_label = frost.LinkedLabel(text="Slidey Value:", widget=slider)
pushbutton = frost.Button(name="Pushy")
linked_label2 = frost.LinkedLabel(text="Pushy Value:", widget=pushbutton)


# Add Widgets to the Frame, from the top down:
frame.add_widget(checkbox1)
frame.add_widget(checkbox2)
frame.add_widget(anchored_label)
frame.add_widget(slider)
frame.add_widget(linked_label)
frame.add_widget(linked_label2)
frame.add_widget(pushbutton)


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
