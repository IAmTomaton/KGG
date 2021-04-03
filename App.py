from PIL import ImageDraw, Image, ImageTk
import tkinter as tk


def draw_dot(draw, pixel, r, color):
    x, y = pixel
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            draw.point((x + dx, y + dy), color)


class App(tk.Tk):

    def __init__(self, size):
        super().__init__()

        self.width, self.height = size

        self._image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        self._photo = ImageTk.PhotoImage(self._image)
        self._label = tk.Label(self, image=self._photo)
        self._label.pack()
        self._image = Image.new('RGB', (self.width, self.height), (255, 255, 255))

    def draw(self, pixels, color=(0, 0, 0), radius=0):
        draw = ImageDraw.Draw(self._image)
        for pixel in pixels:
            draw_dot(draw, pixel, radius, color)
        self._photo = ImageTk.PhotoImage(self._image)
        self._label.configure(image=self._photo)

    def save(self, name='img.png'):
        self._image.save(name)
