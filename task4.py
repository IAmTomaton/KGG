import math
from App import App


def coord_x(x, y, z):
    return (y - x) * math.sqrt(3.0) / 2


def coord_y(x, y, z):
    return (x + y) / 2 - z


def get_pixels(width, height, n, m, f):
    x1 = -3
    x2 = 3
    y1 = -3
    y2 = 3
    top = [height for _ in range(0, width + 1)]
    bottom = [0 for _ in range(0, width + 1)]

    minx = math.inf
    maxx = -minx
    miny = minx
    maxy = maxx

    min_n = max(n, m)
    for i in range(0, min_n):
        x = x2 + i * (x1 - x2) / min_n
        for j in range(0, min_n):
            y = y2 + j * (y1 - y2) / min_n
            z = f(x, y)
            xx = coord_x(x, y, z)
            yy = coord_y(x, y, z)
            if xx > maxx:
                maxx = xx
            if yy > maxy:
                maxy = yy
            if xx < minx:
                minx = xx
            if yy < miny:
                miny = yy

    for i in range(0, n + 1):
        x = x2 + i * (x1 - x2) / n
        for j in range(0, m + 1):
            y = y2 + j * (y1 - y2) / m
            z = f(x, y)
            xx = coord_x(x, y, z)
            yy = coord_y(x, y, z)
            xx = (xx - minx) * width / (maxx - minx)
            yy = (yy - miny) * height / (maxy - miny)
            xx = int(xx)
            yy = int(yy)
            if yy > bottom[xx]:
                yield (xx, yy), True
                bottom[xx] = yy
            if yy < top[xx]:
                yield (xx, yy), False
                top[xx] = yy


def main():
    def f(x, y):
        return math.cos(x * y)

    width, height = 800, 600
    app = App((width, height))

    tuples = get_pixels(width, height, 50, width * 2, f)
    for pix, is_visible in tuples:
        app.draw_dot(pix, (255, 0, 0) if is_visible else (0, 0, 255))

    tuples = get_pixels(width, height, width * 2, 50, f)
    for pix, is_visible in tuples:
        app.draw_dot(pix, (255, 0, 0) if is_visible else (0, 0, 255))

    app.update_image()

    app.save('img.png')
    app.mainloop()


if __name__ == '__main__':
    main()
