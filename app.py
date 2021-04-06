import os
import random

from flask import Flask, render_template

from bouba_kiki import bouba_kiki
from env_setup import env_setup

env_setup()

from drawing.colors import color_palette
from drawing.drawer import draw_svg_design

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route('/palettes')
def palettes():
    palette = color_palette()
    colors = list(map(lambda x: f'rgb({x[0]}, {x[1]}, {x[2]})', palette))
    return '\n'.join(map(lambda x: f"<p style='background-color:{x}'>||||||||</p>", colors)) + f'\n{palette}'


@app.route('/generate/<string:text>')
def logo_generator(text):
    seed = random.randint(0, 4294967295)
    b_coef = bouba_kiki(text)
    params, svg = draw_svg_design(seed=seed,
                                  text=text,
                                  sharpen=b_coef,
                                  color_style="epic")
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
