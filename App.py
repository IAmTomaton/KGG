from PIL import ImageDraw, Image, ImageTk
import tkinter as tk


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
