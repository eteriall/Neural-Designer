from flask import Blueprint, render_template
from numpy import random
from drawing.drawer import draw_svg_design
from bouba_kiki import bouba_kiki

api = Blueprint("api", __name__)


@api.route('/api/generate/<string:text>')
def logo_generator(text):
    seed = random.randint(0, 2_147_483_648)
    b_coef = bouba_kiki(text)
    params, svg = draw_svg_design(seed=seed,
                                  text=text,
                                  sharpen=b_coef,
                                  color_style="epic")
    encoded_output = svg[svg.find('<svg'):]

    return encoded_output


@api.route('/api/save_logo/<int:seed>')
def logo_reciever(seed):
    try:
        params, svg = draw_svg_design(seed=seed)
        return render_template("design.html", svg=svg, data=params)
    except Exception as e:
        pass
    return "Wrong seed", 400
