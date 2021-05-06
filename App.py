from PIL import ImageDraw, Image, ImageTk
import tkinter as tk


def sign(x):
    if x > 0:
        return 1.
    elif x < 0:
        return -1.
    elif x == 0:
        return 0.
    else:
        return x


class App(tk.Tk):

    def __init__(self, size):
        super().__init__()

        self.width, self.height = size

        self._image = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        self._draw = ImageDraw.Draw(self._image)
        self._photo = ImageTk.PhotoImage(self._image)
        self._label = tk.Label(self, image=self._photo)
        self._label.pack()

    def draw(self, pixels, color=(0, 0, 0), radius=0):
        for pixel in pixels:
            self.draw_dot(pixel, color, radius)

    def draw_dot(self, pixel, color=(0, 0, 0), radius=0):
        x, y = pixel
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                self._draw.point((x + dx, y + dy), color)

    def update_image(self):
        self._photo = ImageTk.PhotoImage(self._image)
        self._label.configure(image=self._photo)

    def save(self, name='img.png'):
        self._image.save(name)

    def draw_line(self, xy1, xy2, color=(0, 0, 0), radius=0):
        x1, y1 = int(xy1[0]), int(xy1[1])
        x2, y2 = int(xy2[0]), int(xy2[1])

        length = max(abs(x2 - x1), abs(y2 - y1))
        dx = (x2 - x1) / length
        dy = (y2 - y1) / length
        x = x1 + 0.5 * sign(dx)
        y = y1 + 0.5 * sign(dy)
        i = 0
        while i < length:
            self.draw_dot((x, y), color, radius)
            x += dx
            y += dy
            i += 1

    def draw_polygon(self, vertices, color=(0, 0, 0), radius=0):
        for i in range(0, len(vertices)):
            self.draw_line(vertices[i], vertices[(i + 1) % len(vertices)], color, radius)
