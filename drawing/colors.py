import json
import random

import requests

with open("palettes.json") as f:
    data = json.load(f)["rasskazchikov"]


class Palette:
    def __init__(self, palette=None, convert=False):

        if palette is not None:
            if convert:
                self.palette = list(map(lambda x: tuple(map(lambda y: y / 255, x)), palette))
            else:
                self.palette = palette
        else:
            self.palette = data[random.randint(0, len(data) - 1)]
        self.last_n = 0

    def shuffle(self):
        random.shuffle(self.palette)

    def change_palette(self):
        self.palette = data[random.randint(0, len(data) - 1)]
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


def color_palette(model='default'):
    js = {"model": model}
    palette = requests.get('http://colormind.io/api/', json=js).json()['result']
    return palette

