import itertools
import json
import os
from os import listdir
from os import path

import cairo
import drawSvg as draw
import numpy as np
import svg_stack as ss
from numpy import random

from YandexFlaskProject.vectorizer.png2svg import parse_svg_paths, vectorize
from .colors import Palette

# Load All elements
RESOURCES_DIRECTORY = os.environ.get("RESOURCES_DIR", r"C:\Users\User\PycharmProjects\YandexFlaskProject\YandexFlaskProject\resources")
elements_directory_name = os.environ.get("ELEMENTS_DIR", "")
fonts_file_name = os.environ.get("FONTS_TXT_FILE", "installed_fonts.txt")
palettes_file_name = os.environ.get("PALETTES_JSON_FILE", "palettes.json")
gradients_file_name = os.environ.get("GRADIENTS_JSON_FILE", "gradients.json")
with open(path.join(RESOURCES_DIRECTORY, fonts_file_name)) as fonts_file:
    FONTS = tuple(filter(lambda x: x.strip() != '', fonts_file.read().split('\n')))
with open(path.join(RESOURCES_DIRECTORY, palettes_file_name)) as palettes_file:
    PALETTES = json.load(palettes_file)
with open(path.join(RESOURCES_DIRECTORY, gradients_file_name)) as gradients_file:
    GRADIENTS = json.load(gradients_file)["gradients"]
elements_path = path.join(RESOURCES_DIRECTORY, elements_directory_name)
ELEMENTS = [f for f in listdir(elements_path) if path.isfile(path.join(elements_path, f))]


class LogoData:
    def __init__(self, **kwargs):
        self.seed = kwargs.get("seed", 0)
        self.text_color = kwargs.get("text_color", (0, 0, 0))
        self.text_font = kwargs.get("text_font", "Dela Gothic One")

    def jsonify(self):
        return {"text_font": self.text_font,
                "text_color": self.text_color,
                "seed": self.seed}

    def __call__(self, *args, **kwargs):
        self.jsonify()


class Style(draw.DrawingDef):
    TAG_NAME = "style"

    def __init__(self, import_statement, **kwargs):
        self.import_statement = import_statement
        super().__init__(**kwargs, type="text/css")

    def writeSvgElement(self, idGen, isDuplicate, outputFile, dryRun, forceDup=False):
        outputFile.write(f'<style type="text/css">{self.import_statement}</style>')


class ImportStatement(draw.DrawingBasicElement):
    pass


def get_recolored_element(element_name, color):
    with open(element_name) as f:
        data = f.read()
        data.replace("black", color)
        return None


# deprecated def
def draw_logo_legacy(palette: Palette,
                     file_name: str = 'example.png',
                     add_svg_elements: bool = False,
                     rects_max_n: int = 2,
                     poly_max_n: int = 4,
                     color_style: str = 'smooth',
                     sharpen: float = 0.5,
                     image_size: tuple = (512, 512)):
    # Create svg surface
    with cairo.SVGSurface(file_name, image_size[0], image_size[1]) as surface:

        ctx = cairo.Context(surface)
        ctx.scale(image_size[0], image_size[1])

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

        #
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
        text_x, text_y = random.randint(0, image_size[0] // 4), random.randint(0 + 200, image_size[1] - 200)
        Context.move_to(text_x, text_y)

        Context.set_source_rgb(0, 0, 0)
        Context.text_path("NTI")

        svg = vectorize(public_id='yd0cnq0dxzgjscg1afct')
        path = parse_svg_paths(svg)[-1][9:-3]

        Context.append_path(cairo.Path(path))
        Context.stroke()

        # Fill text
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
    if add_svg_elements:
        doc = ss.Document()

        layout1 = ss.HBoxLayout()
        layout1.setSpacing(-image_size[0])
        layout1.addSVG(file_name, alignment=ss.AlignHCenter | ss.AlignVCenter)
        for _ in range(1):
            el = random.choice(ELEMENTS)
            layout1.addSVG(el, alignment=ss.AlignHCenter | ss.AlignVCenter)
        doc.setLayout(layout1)
        doc.save(file_name)


def draw_svg_design(file_name: str = 'example.png',
                    text="Template",
                    add_svg_elements: bool = False,
                    rects_max_n: int = 2,
                    poly_max_n: int = 2,
                    circles_max_n: int = 2,
                    poly_max_n_points: int = 4,
                    color_style: str = 'smooth',
                    font_color: tuple = (0, 0, 0),
                    sharpen: float = 0.5,
                    font_family: str or None = None,
                    image_size: tuple = (512, 512),
                    margin: tuple = (50, 50),
                    seed=None) -> tuple:
    if seed is not None:
        random.seed(seed)
    if font_family is None:
        font_family = random.choice(FONTS)

    p = Palette(color_style)
    d = draw.Drawing(image_size[0], image_size[1], displayInline=False)

    import_statement = Style('@import url(http://fonts.googleapis.com/css?family=Dela+Gothic+One);')
    d.append(import_statement)

    poly_max_n += int(poly_max_n * sharpen)

    # Drawing polygons
    for _ in range(0, poly_max_n):
        # Generating points for polygon
        points_ = [(random.randint(0 + margin[0], image_size[0] - margin[0]),
                    random.randint(0 + margin[1], image_size[1] - margin[1]))
                   for _ in range(random.randint(3, poly_max_n_points))]

        # Concatenating all coordinates
        points = list(itertools.chain(*points_))

        poly_params = {}
        if random.random() < 0.6:
            poly_params["fill"] = p.next_rgb()
        else:
            poly_params["stroke"] = p.next_rgb()
            poly_params["stroke_width"] = random.randint(3, 10)
            poly_params["fill"] = "rgba(0, 0, 0, 0.001)"
        if sharpen < 0:
            poly_params['stroke-linejoin'] = "round"
        elif sharpen > 0:
            poly_params['stroke-linejoin'] = "miter"
        else:
            poly_params['stroke-linejoin'] = "round" if random.random() > 0.5 else "miter"
        # Drawing
        d.append(draw.Lines(*points,
                            close=True,
                            **poly_params))

    circles_max_n += int(circles_max_n * -sharpen)

    for _ in range(circles_max_n):

        circle_params = {}
        if random.random() < 0.6:
            circle_params["fill"] = p.next_rgb()
        else:
            circle_params["stroke"] = p.next_rgb()
            circle_params["stroke_width"] = random.randint(3, 6)
            circle_params["fill"] = "rgba(0, 0, 0, 0.001)"

        s = random.randint(30, 100)
        cx, cy = random.randint(margin[0], image_size[0] - s // 2), random.randint(margin[1], image_size[1] - s // 2)
        circle = draw.Circle(cx, cy, s, **circle_params)
        d.append(circle)

    # Draw text
    r, g, b = font_color
    font_size = random.randint(70, 150)
    x, y = random.randint(margin[0], image_size[0] // 2), random.randint(margin[1] * 2, image_size[1] - margin[1] * 2)
    d.append(draw.Text(text, font_size, x, y, fill=f'rgb({r}, {g}, {b})', font_family=font_family))
    svg = vectorize(public_id='yd0cnq0dxzgjscg1afct')
    path = parse_svg_paths(svg)[-1][9:-3]
    d.append(draw.Path(path, stroke="black"))
    ret_params = {'font_color': font_color,
                  'font_family': font_family,
                  'seed': seed,
                  'circles_n': circles_max_n,
                  'poly_n': poly_max_n,
                  'sharpen': sharpen,
                  'font_size': font_size}

    """ # Draw a rectangle
    

    # Draw a circle
    d.append(draw.Circle(-40, -10, 30,
                         fill='red', stroke_width=2, stroke='black'))

    # Draw an arbitrary path (a triangle in this case)
    p = draw.Path(stroke_width=2, stroke='lime',
                  fill='black', fill_opacity=0.2)
    p.M(-10, 20)  # Start path at point (-10, 20)
    p.C(30, -10, 30, 50, 70, 20)  # Draw a curve to (70, 20)
    d.append(p)

    
    d.append(draw.Text('Path text', 8, path=p, text_anchor='start', valign='middle'))
    d.append(draw.Text(['Multi-line', 'text'], 8, path=p, text_anchor='end'))

    # Draw multiple circular arcs
    d.append(draw.ArcLine(60, -20, 20, 60, 270,
                          stroke='red', stroke_width=5, fill='red', fill_opacity=0.2))
    d.append(draw.Arc(60, -20, 20, 60, 270, cw=False,
                      stroke='green', stroke_width=3, fill='none'))
    d.append(draw.Arc(60, -20, 20, 270, 60, cw=True,
                      stroke='blue', stroke_width=1, fill='black', fill_opacity=0.3))

    # Draw arrows
    arrow = draw.Marker(-0.1, -0.5, 0.9, 0.5, scale=4, orient='auto')
    arrow.append(draw.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill='red', close=True))
    p = draw.Path(stroke='red', stroke_width=2, fill='none',
                  marker_end=arrow)  # Add an arrow to the end of a path
    p.M(20, -40).L(20, -27).L(0, -20)  # Chain multiple path operations
    d.append(p)
    d.append(draw.Line(30, -20, 0, -10,
                       stroke='red', stroke_width=2, fill='none',
                       marker_end=arrow))  # Add an arrow to the end of a line

    d.setPixelScale(2)  # Set number of pixels per geometry unit
    # d.setRenderSize(400,200)  # Alternative to setPixelScale"""
    return ret_params, d.asSvg()


def generate_variations(p, n=10):
    for i in range(n):
        draw_logo_legacy(p, file_name=f'images/{i}.svg', rects_max_n=3, poly_max_n=4)
        p.change_palette()

