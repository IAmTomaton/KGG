from PIL import ImageDraw, Image, ImageTk
import tkinter as tk


def draw_dot(draw, pixel, r):
    x, y = pixel
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            draw.point((x + dx, y + dy), (0, 0, 0))


class App(tk.Tk):

    def __init__(self, size):
        super().__init__()

        self.width, self.height = size

        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        self._photo = ImageTk.PhotoImage(image)
        self._label = tk.Label(self, image=self._photo)
        self._label.pack()

    def draw(self, pixels, radius=0):
        image = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        for pixel in pixels:
            draw_dot(draw, pixel, radius)
        self._photo = ImageTk.PhotoImage(image)
        self._label.configure(image=self._photo)
        image.save('img.png')
