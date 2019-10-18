from functools import lru_cache as _lru_cache


# Helper functions for creating verts and colors:

@_lru_cache()
def _create_left(x, y, width, height, color1, color2):
    one = x, y
    two = x, y + height
    three = x + width, y + height - width
    four = x + width, y + width
    verts = one + two + three + three + one + four
    colors = color1 + color1 + color2 + color2 + color1 + color2
    return verts, colors


@_lru_cache()
def _create_right(x, y, width, height, color1, color2):
    one = x, y + width
    two = x, y + height - width
    three = x + width, y + height
    four = x + width, y
    verts = one + two + three + three + one + four
    colors = color1 + color1 + color2 + color2 + color1 + color2
    return verts, colors


@_lru_cache()
def _create_bottom(x, y, width, height, color1, color2):
    one = x, y
    two = x + width, y
    three = x + width - height, y + height
    four = x + height, y + height
    verts = one + two + three + three + one + four
    colors = color1 + color1 + color2 + color2 + color1 + color2
    return verts, colors


@_lru_cache()
def _create_top(x, y, width, height, color1, color2):
    one = x + height, y
    two = x + width - height, y
    three = x + width, y + height
    four = x, y + height
    verts = one + two + three + three + one + four
    colors = color1 + color1 + color2 + color2 + color1 + color2
    return verts, colors


@_lru_cache()
def _create_frame_top(x, y, width, height, menusize, color1, color2):
    one = x + height, y - menusize
    two = x + width - height, y - menusize
    three = x + width, y + height
    four = x, y + height
    verts = one + two + three + three + one + four
    colors = color1 + color1 + color2 + color2 + color1 + color2
    return verts, colors


@_lru_cache()
def _create_center(x, y, width, height, color):
    one = x, y
    two = x + width, y
    three = x + width, y + height
    four = x, y + height
    verts = one + two + three + three + one + four
    colors = color * 6
    return verts, colors


@_lru_cache()
def _line_box(x, y, width, height, color):
    one = x, y
    two = x + width, y
    three = x + width, y + height
    four = x, y + height
    verts = one + two + two + three + three + four + four + one
    colors = color * 8
    return verts, colors


# Pre-defined objects:

def frame(x, y, width, height, border=2, menusize=10, color1=(25, 25, 25), color2=(50, 50, 50)):
    b = border
    m = menusize
    bottom, bottom_c = _create_bottom(x, y, width, border, color1, color2)
    left, left_c = _create_left(x, y, border, height, color1, color2)
    right, right_c = _create_right(x + width - b, y, border, height, color2, color1)
    top, top_c = _create_frame_top(x, y + height - b, width, b, m, color2, color1)

    return bottom + left + right + top, bottom_c + left_c + right_c + top_c


def checkbox(x, y, width, height, border, color1=(150, 150, 150), color2=(100, 100, 100), checked=True):
    w = width
    h = height
    b = border

    bottom, bottom_c = _create_bottom(x, y, width, border, color1, color2)
    left, left_c = _create_left(x, y, border, height, color1, color2)
    right, right_c = _create_right(x + width - b, y, border, height, color2, color1)
    top, top_c = _create_top(x, y + h - b, width, border, color2, color1)
    center_color = (150,) if checked else (0,)
    center, center_c = _create_center(x + b, y + b, w - b*2, h - b*2, color=center_color * 3)

    verts = bottom + left + right + top + center
    colors = bottom_c + left_c + right_c + top_c + center_c

    return verts, colors


def slider(x, y, width, height, bar, color1=(150, 150, 150), color2=(100, 100, 100), position=0):
    w = width
    h = height
    bar_offset = height // 2 - bar // 2

    track, track_c = _create_center(x, y + bar_offset, w, bar, color1)
    knob, knob_c = _create_center(position, y, h//2, h, color2)

    verts = track + knob
    colors = track_c + knob_c

    return verts, colors


def textbox(x, y, width, height, color=(150, 150, 150)):
    return _line_box(x, y, width, height, color)


def button(x, y, width, height, color1=(100, 100, 100), color2=(150, 150, 150), pressed=True):
    b = height / 2
    c1 = color2 if pressed else color1
    c2 = color1 if pressed else color2

    bottom, bottom_c = _create_bottom(x, y, width, b, c1, c2)
    left, left_c = _create_left(x, y, b, height, c1, c2)
    right, right_c = _create_right(x + width - b, y, b, height, c2, c1)
    top, top_c = _create_top(x, y + height - b, width, b, c2, c1)

    verts = bottom + left + right + top
    colors = bottom_c + left_c + right_c + top_c

    return verts, colors
