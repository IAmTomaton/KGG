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


def get_min_max_y(f, interval, width):
    a, b = interval[0], interval[1]
    miny = maxy = f(a)
    for xx in range(width):
        x = a + xx * (b - a) / width
        y = f(x)
        if y < miny:
            miny = y
        if y > maxy:
            maxy = y
    return miny, maxy


def pixels_by_parabola_bresenham(a, b, c, width, Ox, Oy):
    p = - (b * b) / a
    x0 = a + c
    y0 = 0
    yield x0 + Ox, y0 + Oy
    x = 0
    y = 0
    x_dir = -sign(a)
    Sd = ((y + 1) * (y + 1)) - p * (x + x_dir)
    Sv = ((y + 1) * (y + 1)) - p * x
    Sh = (y * y) - p * (x + x_dir)
    while (x + x0 + Ox < width and x_dir > 0) or (0 < x + x0 + Ox and x_dir < 0):
        if abs(Sh) - abs(Sv) <= 0:
            if abs(Sd) - abs(Sh) < 0:
                y += 1
            x += x_dir
        else:
            if abs(Sv) - abs(Sd) > 0:
                x += x_dir
            y += 1

        yield x + x0 + Ox, y + y0 + Oy
        yield x + x0 + Ox, -y + y0 + Oy

        Sd = ((y + 1) * (y + 1)) - p * (x + x_dir)
        Sv = ((y + 1) * (y + 1)) - p * x
        Sh = (y * y) - p * (x + x_dir)


def pixels_by_line(xy1, xy2):
    x1, y1 = int(xy1[0]), int(xy1[1])
    x2, y2 = int(xy2[0]), int(xy2[1])

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


def main():
    width, height = 640, 640
    a = 1
    b = 10
    c = -10

    Oy = height / 2
    Ox = 0 if a < 0 else width - 1

    app = App((width, height))

    app.draw(pixels_by_line((Ox, 0), (Ox, height)), color=(150, 0, 150))

    app.draw(pixels_by_line((0, Oy), (width, Oy)), color=(150, 150, 0))

    pixels = pixels_by_parabola_bresenham(a, b, c, width, Ox, Oy)
    app.draw(pixels)

    app.update_image()

    app.save('img.png')
    app.mainloop()


if __name__ == '__main__':
    main()
