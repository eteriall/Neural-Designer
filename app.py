import os
import random

from flask import Flask, request, g, render_template, Blueprint, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from bouba_kiki import bouba_kiki
from config import env_setup

env_setup()

from drawing.colors import color_palette
from drawing.drawer import draw_svg_design
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

app = Flask(__name__)
app.config["LANGUAGES"] = {
    'en': 'English',
    'ru': 'Русский'
}
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
db = SQLAlchemy()
babel = Babel(app)

web_interface = Blueprint('web_interface', __name__)


@babel.localeselector
def get_locale():
    if not g.get('lang_code', None):
        g.lang_code = request.accept_languages.best_match(app.config['LANGUAGES'])
    return g.lang_code


@app.before_request
def before():
    args = dict(request.args)
    if args and 'lang_code' in args:
        if args['lang_code'] in ('ru', 'en'):
            g.lang_code = args['lang_code']
    else:
        if not g.get('lang_code', None):
            g.lang_code = request.accept_languages.best_match(app.config['LANGUAGES'])

@web_interface.route("/")
def index():
    return render_template("index.html", lang_code="ru")


@web_interface.route("/about")
def about():
    return render_template("about.html")


@web_interface.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']

    return render_template("login.html")


@web_interface.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
    return render_template("register.html")


@web_interface.route('/palettes')
def palettes():
    palette = color_palette()
    colors = list(map(lambda x: f'rgb({x[0]}, {x[1]}, {x[2]})', palette))
    return '\n'.join(map(lambda x: f"<p style='background-color:{x}'>||||||||</p>", colors)) + f'\n{palette}'


@web_interface.route('/generate/<string:text>')
def logo_generator(text):
    seed = random.randint(0, 4294967295)
    b_coef = bouba_kiki(text)
    params, svg = draw_svg_design(seed=seed,
                                  text=text,
                                  sharpen=b_coef,
                                  color_style="epic")
    encoded_output = svg[svg.find('<svg'):]

    return render_template("design.html", svg=encoded_output, data=params)


@web_interface.route('/save_logo/<int:seed>')
def logo_reciever(seed):
    try:
        params, svg = draw_svg_design(seed=seed)
        return render_template("design.html", svg=svg, data=params)
    except Exception as e:
        pass
    return "Wrong seed", 400


if __name__ == "__main__":
    app.register_blueprint(web_interface)
    app.run()
