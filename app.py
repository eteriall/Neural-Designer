import os
import random

from flask import Flask, render_template

from env_setup import env_setup

env_setup()

from drawing.colors import color_palette
from drawing.drawer import draw_svg_design

app = Flask(__name__)


@app.route('/palettes')
def palettes():
    palette = color_palette()
    colors = list(map(lambda x: f'rgb({x[0]}, {x[1]}, {x[2]})', palette))
    return '\n'.join(map(lambda x: f"<p style='background-color:{x}'>asdf</p>", colors)) + f'\n{palette}'


@app.route('/generate')
def logo_generator():
    seed = random.randint(0, 4294967295)
    params, svg = draw_svg_design(seed=seed)
    encoded_output = svg[svg.find('<svg'):]
    return render_template("design.html", svg=encoded_output, data=params)


@app.route('/save_logo/<int:seed>')
def logo_reciever(seed):
    try:
        params, svg = draw_svg_design(seed=seed)
        return render_template("design.html", svg=svg, data=params)
    except Exception as e:
        pass
    return "Wrong seed", 400


if __name__ == "__main__":
    app.run()
