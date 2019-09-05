from math import *


# def make_circle(x, y, radius, color1, color2, steps=10):
#     b = radius
#     c1 = color1
#     c2 = color2
#     points = []
#
#     for i in range(0, 361, steps):
#         r = -radians(i)
#         points.extend((round(cos(r), 3), round(sin(r), 3)))
#
#     vertices = []
#     colors = []
#     last = None
#
#     for point in zip(points[0::2], points[1::2]):
#         if not last:
#             last = point
#             continue
#         triangle = x, y, x+last[0]*b, y+last[1]*b, x+point[0]*b, y+point[1]*b
#         color = c1 + c2 + c2
#         vertices.extend(triangle)
#         colors.extend(color)
#         last = point
#
#     return vertices, colors
#
#
# def make_dot_circle(x, y, radius, color1, color2, steps=10):
#     b = radius
#     c1 = color1
#     c2 = color2
#     inner_points = []
#
#     for i in range(0, 361, steps):
#         r = -radians(i)
#         inner_points.extend((round(cos(r), 3), round(sin(r), 3)))
#
#     vertices = []
#     colors = []
#     last = None
#
#     for point in zip(inner_points[0::2], inner_points[1::2]):
#         if not last:
#             last = point
#             continue
#         triangle = x, y, x+last[0]*b, y+last[1]*b, x+point[0]*b, y+point[1]*b
#         color = c1 + c2 + c2
#
#         vertices.extend(triangle)
#         colors.extend(color)
#         last = point
#
#     return vertices, colors
#
#
# def make_corner(x, y, start_deg, end_deg, border_width, color1, color2):
#     b = border_width
#     c1 = color1
#     c2 = color2
#     points = []
#
#     for i in range(start_deg, end_deg+1, 15):
#         r = -radians(i)
#         points.extend((round(cos(r), 3), round(sin(r), 3)))
#
#     vertices = []
#     colors = []
#     last = None
#
#     for point in zip(points[0::2], points[1::2]):
#         if not last:
#             last = point
#             continue
#         triangle = x, y, x+last[0]*b, y+last[1]*b, x+point[0]*b, y+point[1]*b
#         color = c1 + c2 + c2
#         vertices.extend(triangle)
#         colors.extend(color)
#         last = point
#
#     return vertices, colors


def create_left_right(x, y, width, height, color1, color2):
    verts = x, y, x + width, y, x + width, y + height, x + width, y + height, x, y + height, x, y
    colors = color1 + color2 + color2 + color2 + color1 + color1
    return verts, colors


def create_top_bottom(x, y, width, height, color1, color2):
    verts = x, y, x + width, y, x + width, y + height, x + width, y + height, x, y + height, x, y
    colors = color1 + color1 + color2 + color2 + color2 + color1
    return verts, colors


def _create_left(x, y, width, height, color1, color2):
    one = x, y
    two = x, y + height
    three = x + width, y + height - width
    four = x + width, y + width
    verts = one + two + three + three + one + four
    colors = color1 + color1 + color2 + color2 + color1 + color2
    return verts, colors


def _create_right(x, y, width, height, color1, color2):
    one = x, y + width
    two = x, y + height - width
    three = x + width, y + height
    four = x + width, y
    verts = one + two + three + three + one + four
    colors = color1 + color1 + color2 + color2 + color1 + color2
    return verts, colors


def _create_bottom(x, y, width, height, color1, color2):
    one = x, y
    two = x + width, y
    three = x + width - height, y + height
    four = x + height, y + height
    verts = one + two + three + three + one + four
    colors = color1 + color1 + color2 + color2 + color1 + color2
    return verts, colors


def _create_top(x, y, width, height, color1, color2):
    one = x + height, y
    two = x + width - height, y
    three = x + width, y + height
    four = x, y + height
    verts = one + two + three + three + one + four
    colors = color1 + color1 + color2 + color2 + color1 + color2
    return verts, colors


def _create_center(x, y, width, height, color):
    one = x, y
    two = x + width, y
    three = x + width, y + height
    four = x, y + height
    verts = one + two + three + three + one + four
    colors = color * 6
    return verts, colors

# def calculate_bottom(x, y, width, height, border, color1,  color2):
#     b = border
#     verts = [x, y,  x + width, y,  x + width - b, y + height,
#              x + width, y + height,  x + b, y + height,  x, y]
#     colors = list(color1 + color1 + color2 + color2 + color2 + color1)
#     return verts, colors
#
#
# def calculate_top(x, y, width, height, border, color1, color2):
#     b = border
#     verts = [x + width, y + height,  x + b, y + height,  x, y,
#              x, y,  x + width, y,  x + width - b, y + height]
#     colors = list(color1 + color1 + color2 + color2 + color2 + color1)
#     return verts, colors
#
#
# def calculate_frame(x, y, width, height, border=2, menusize=10, color1=(25, 25, 25), color2=(50, 50, 50)):
#     b = border
#     m = menusize
#
#     tlcv, tlcc = make_corner(x+b, y+height-b, 180, 270, border, color1, color2)
#     trcv, trcc = make_corner(x+width-b, y+height-b, 270, 360, border, color1, color2)
#     brcv, brcc = make_corner(x+width-b, y+b, 0, 90, border, color1, color2)
#     blcv, blcc = make_corner(x+b, y+b, 90, 180, border, color1, color2)
#
#     tb, tc = create_top_bottom(x + b, y + height - m, width - b - b, m, color1, color2)
#
#     lb, lc = create_left_right(x, y + b, b, height - b - b, color2, color1)
#     rb, rc = create_left_right(x + width - b, y + b, b, height - b - b, color1, color2)
#
#     bb, bc = create_top_bottom(x + b, y, width - b - b, b, color2, color1)
#     # bb, bc = calculate_bottom(x, y, width, b, border, color2, color1)
#
#     vertices = brcv + blcv + tlcv + trcv + lb + bb + rb + tb
#     colors = brcc + blcc + tlcc + trcc + lc + bc + rc + tc
#
#     return vertices, colors


def simple_frame(x, y, width, height, border=2, menusize=10, color1=(25, 25, 25), color2=(50, 50, 50)):
    w = width
    h = height
    b = border
    m = menusize
    c1 = color1
    c2 = color2

    bottom = x, y, x+w, y, x+w, y+b,  x, y, x+w, y+b, x, y+b
    bottom_c = c2 + c2 + c2 + c2 + c2 + c2
    left = x, y+b, x+b, y+b, x+b, y+h-m,  x+b, y+h-m, x, y+h-m, x, y+b
    left_c = c1 + c2 + c2 + c2 + c1 + c1
    right = x+w-b, y+b,   x+w, y+b,   x+w, y+h-m,    x+w, y+h-m, x+w-b, y+h-m, x+w-b, y+b
    right_c = c2 + c1 + c1 + c1 + c2 + c2
    top = x, y+h-m, x+w, y+h-m, x+w, y+h,  x+w, y+h, x, y+h, x, y+h-m
    top_c = c2 + c2 + c1 + c1 + c1 + c2

    return bottom + left + right + top, bottom_c + left_c + right_c + top_c


def checkbox(x, y, width, height, border, color1=(25, 25, 25), color2=(50, 50, 50)):
    w = width
    h = height
    b = border

    bottom, bottom_c = _create_bottom(x, y, width, border, color1, color2)
    left, left_c = _create_left(x, y, border, height, color1, color2)
    right, right_c = _create_right(x + width - b, y, border, height, color2, color1)
    top, top_c = _create_top(x, y + h - b, width, border, color2, color1)

    # TODO: make center segment. Not working yet.
    # center, center_c = _create_center(x + b, y + b, w - b, height - b, color=(0, 255, 0))

    verts = bottom + left + right + top
    colors = bottom_c + left_c + right_c + top_c

    return verts, colors
