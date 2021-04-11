import json
from os import environ, path

import numpy.random as random

import requests


class Palette:
    def __init__(self,
                 palette_name: str = 'smooth',
                 convert: int = False, seed=random.randint(0, 100000)):
        with open(path.join(environ.get("RESOURCES_DIR", r"C:\Users\User\PycharmProjects\YandexFlaskProject\YandexFlaskProject\resources"),
                            environ.get("PALETTES_JSON_FILE", "palettes.json"))) as palettes_file:
            self.palettes = json.load(palettes_file)[palette_name]
        if convert:
            self.palette = list(map(lambda x: tuple(map(lambda y: y / 255, x)), self.palettes))
        else:
            self.palette = self.palettes[random.randint(0, len(self.palettes) - 1)]
        self.last_n = 0

    def shuffle(self):
        random.shuffle(self.palette)

    def change_palette(self):
        self.palette = self.palettes[random.randint(0, len(self.palettes) - 1)]
        self.palette = list(map(lambda x: tuple(map(lambda y: y / 255, x)), self.palette))

    def __getitem__(self, item):
        return self.palette[item % len(self.palette)]

    def next(self, exclude=()):
        self.last_n += 1
        l = self.palette[self.last_n % len(self.palette)]
        while l == exclude:
            self.last_n += 1
            l = self.palette[self.last_n % len(self.palette)]
        return l

    def next_rgb(self):
        r, g, b = self.next()
        return f"rgb({r}, {g}, {b})"


def color_palette(model='default'):
    js = {"model": model}
    palette = requests.get('http://colormind.io/api/', json=js).json()['result']
    return palette
