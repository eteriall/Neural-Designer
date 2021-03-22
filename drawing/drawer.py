import json
import math
from time import time
import io
import cairo
import numpy as np
from numpy import random
from random import choice
import svg_stack as ss

from os import listdir
from os.path import isfile, join

from colors import color_palette, Palette

FONTS = ["Skybird", "KBTrueBeliever", "KBPayTheLady"]
ELEMENTS = [join('elements', f) for f in listdir('elements') if isfile(join('elements', f))]
with open("gradients.json") as f:
    GRADIENTS = json.load(f)["gradients"]


def get_recolored_element(element_name, color):
    with open(element_name) as f:
        data = f.read()
        data.replace("black", color)
        return None


def draw_logo(palette: Palette, fname='example.png', add_elems=False, rects_max_n=2, poly_max_n=4):
    WIDTH, HEIGHT = 512, 512
    with cairo.SVGSurface(fname, WIDTH, HEIGHT) as surface:

        ctx = cairo.Context(surface)
        ctx.scale(WIDTH, HEIGHT)

        """ctx.rectangle(0, 0, 1, 1)
        c = palette.next()
        bg = c
        ctx.set_source_rgb(*c)
        ctx.fill()"""

        r = [cairo.LINE_JOIN_MITER, cairo.LINE_JOIN_BEVEL, cairo.LINE_JOIN_ROUND]
        ctx.set_line_join(random.choice(r))

        for _ in range(rects_max_n):
            x, y = random.random(), random.random()
            ctx.rectangle(x, y, random.random(), random.random())
            c = palette.next()
            ctx.set_source_rgb(*c)
            ctx.fill()

        for _ in range(random.randint(poly_max_n // 2, poly_max_n)):
            points = [(random.random(), random.random()) for _ in range(random.randint(3, 5))]

            if random.random() < 0.5:
                ctx.curve_to(*np.array(points[:3]).flatten())
            else:
                ctx.move_to(*points[0])
                for point in points[1:]:
                    ctx.line_to(*point)

            ctx.close_path()
            if random.random() < 0.7:
                ctx.set_source_rgb(*palette.next())
            else:
                gr = GRADIENTS[random.randint(0, len(GRADIENTS))]
                lg1 = cairo.LinearGradient(*points[0], *points[-1])
                lg1.add_color_stop_rgb(0, *map(lambda x: x / 255, gr[0]))
                lg1.add_color_stop_rgb(0.5, *map(lambda x: x / 255, gr[1]))
                ctx.set_source(lg1)

            ctx.set_line_width(random.randint(1, 10) / 100)
            if random.random() < 0.6:
                ctx.stroke()
            else:
                ctx.fill()

        Context = cairo.Context(surface)
        Context.set_font_size(100)
        Context.select_font_face(random.choice(FONTS), cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        text_x, text_y = random.randint(0, WIDTH // 4), random.randint(0 + 200, HEIGHT - 200)
        Context.move_to(text_x, text_y)

        Context.text_path("letaem")

        if random.random() > 0.7:
            gr = GRADIENTS[random.randint(0, len(GRADIENTS))]
            lg1 = cairo.LinearGradient(text_x, text_y, 500, 500)
            lg1.add_color_stop_rgb(0, *map(lambda x: x / 255, gr[0]))
            lg1.add_color_stop_rgb(0.5, *map(lambda x: x / 255, gr[1]))
            Context.set_source(lg1)
        else:
            Context.set_source_rgb(0, 0, 0)
        if random.random() < 0.6:
            Context.fill()
        else:
            Context.stroke()
    if add_elems:
        doc = ss.Document()

        layout1 = ss.HBoxLayout()
        layout1.setSpacing(-WIDTH)
        layout1.addSVG(fname, alignment=ss.AlignHCenter | ss.AlignVCenter)
        for _ in range(1):
            el = random.choice(ELEMENTS)
            layout1.addSVG(el, alignment=ss.AlignHCenter | ss.AlignVCenter)
        doc.setLayout(layout1)
        doc.save(fname)


def generate_variations(p, n=10):
    for i in range(n):
        draw_logo(p, fname=f'images/{i}.svg', rects_max_n=0, poly_max_n=4)
        p.change_palette()


t = time()
p = Palette(convert=True)
generate_variations(p, n=100)
print(time() - t)
