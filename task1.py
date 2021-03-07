import math
from App import App


def sign(x):
    if x > 0:
        return 1.
    elif x < 0:
        return -1.
    elif x == 0:
        return 0.
    else:
        return x


def points_by_func(f, interval, width, height):
    a, b = interval[0], interval[1]
    miny = maxy = f(a)
    for xx in range(width):
        x = a + xx * (b - a) / width
        y = f(x)
        if y < miny:
            miny = y
        if y > maxy:
            maxy = y
    yy = (f(a) - miny) * height / (maxy - miny)
    # yy = (f(a) - miny) * width / (b - a)
    yield 0, height - yy
    for xx in range(1, width):
        x = a + xx * (b - a) / width
        yy = (f(x) - miny) * height / (maxy - miny)
        # yy = (f(x) - miny) * width / (b - a)
        yield xx, height - yy


def pixels_by_line(a, b):
    x1, y1 = a[0], a[1]
    x2, y2 = b[0], b[1]

    length = max(abs(x2 - x1), abs(y2 - y1))
    dx = (x2 - x1) / length
    dy = (y2 - y1) / length
    x = x1 + 0.5 * sign(dx)
    y = y1 + 0.5 * sign(dy)
    i = 0
    while i < length:
        yield x, y
        x += dx
        y += dy
        i += 1


def get_pixels(func, width, height, a, b):
    prev = None
    for point in points_by_func(func, (a, b), width, height):
        if not prev:
            prev = point
            continue
        for pixel in pixels_by_line(prev, point):
            yield pixel
        prev = point


def main():
    def f(x):
        return x * math.sin(x)
    a, b = -10, 10
    width, height = 640, 640
    app = App((width, height))

    pixels = get_pixels(f, width, height, a, b)
    app.draw(pixels)

    app.mainloop()


if __name__ == '__main__':
    main()
