from math import *


def make_circle(x, y, radius, color1, color2, steps=10):
    b = radius
    c1 = color1
    c2 = color2
    points = []

    for i in range(0, 361, steps):
        r = -radians(i)
        points.extend((round(cos(r), 3), round(sin(r), 3)))

    vertices = []
    colors = []
    last = None

    for point in zip(points[0::2], points[1::2]):
        if not last:
            last = point
            continue
        triangle = x, y, x+last[0]*b, y+last[1]*b, x+point[0]*b, y+point[1]*b
        color = c1 + c2 + c2
        vertices.extend(triangle)
        colors.extend(color)
        last = point

    return vertices, colors


def make_corner(x, y, start_deg, end_deg, border_width, color1, color2):
    b = border_width
    c1 = color1
    c2 = color2
    points = []

    for i in range(start_deg, end_deg+1, 15):
        r = -radians(i)
        points.extend((round(cos(r), 3), round(sin(r), 3)))

    vertices = []
    colors = []
    last = None

    for point in zip(points[0::2], points[1::2]):
        if not last:
            last = point
            continue
        triangle = x, y, x+last[0]*b, y+last[1]*b, x+point[0]*b, y+point[1]*b
        color = c1 + c2 + c2
        vertices.extend(triangle)
        colors.extend(color)
        last = point

    return vertices, colors


def create_left_right(x, y, width, height, color1, color2):
    verts = [x, y, x + width, y, x + width, y + height, x + width, y + height, x, y + height, x, y]
    colors = list(color1 + color2 + color2 + color2 + color1 + color1)
    return verts, colors


def create_top_bottom(x, y, width, height, color1, color2):
    verts = [x, y, x + width, y, x + width, y + height, x + width, y + height, x, y + height, x, y]
    colors = list(color1 + color1 + color2 + color2 + color2 + color1)
    return verts, colors


def calculate_bottom(x, y, width, height, border, color1,  color2):
    b = border
    verts = [x, y,  x + width, y,  x + width - b, y + height,
             x + width, y + height,  x + b, y + height,  x, y]
    colors = list(color1 + color1 + color2 + color2 + color2 + color1)
    return verts, colors


def calculate_top(x, y, width, height, border, color1, color2):
    b = border
    verts = [x + width, y + height,  x + b, y + height,  x, y,
             x, y,  x + width, y,  x + width - b, y + height]
    colors = list(color1 + color1 + color2 + color2 + color2 + color1)
    return verts, colors


def calculate_frame(x, y, width, height, border=2, menusize=10, color1=(25, 25, 25), color2=(50, 50, 50)):
    b = border
    m = menusize

    tlcv, tlcc = make_corner(x+b, y+height-b, 180, 270, border, color1, color2)
    trcv, trcc = make_corner(x+width-b, y+height-b, 270, 360, border, color1, color2)
    brcv, brcc = make_corner(x+width-b, y+b, 0, 90, border, color1, color2)
    blcv, blcc = make_corner(x+b, y+b, 90, 180, border, color1, color2)

    tb, tc = create_top_bottom(x + b, y + height - m, width - b - b, m, color1, color2)

    lb, lc = create_left_right(x, y + b, b, height - b - b, color2, color1)
    rb, rc = create_left_right(x + width - b, y + b, b, height - b - b, color1, color2)

    bb, bc = create_top_bottom(x + b, y, width - b - b, b, color2, color1)
    # bb, bc = calculate_bottom(x, y, width, b, border, color2, color1)

    vertices = brcv + blcv + tlcv + trcv + lb + bb + rb + tb
    colors = brcc + blcc + tlcc + trcc + lc + bc + rc + tc

    return vertices, colors