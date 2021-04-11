import os
import random

from flask import Flask, request, g, render_template, Blueprint, url_for, session
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

from forms.survey1_form import SurveyForm
from forms.registration_form import RegistrationForm
from data.users import User
from bouba_kiki import bouba_kiki
from config import env_setup
import flask

env_setup()
from flask_login import LoginManager
from data import db_session
from drawing.colors import color_palette
from drawing.drawer import draw_svg_design
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, lazy_gettext
from forms.login_form import LoginForm
from flask_session import Session

app = Flask(__name__)
db_session.global_init(
    "postgresql://ofsxjjrazrzyds:6d167a663668124bb6815c31c79f350e0c05d9dff940870db58521e08306dc4d@ec2-34-254-69-72.eu-west-1.compute.amazonaws.com:5432/d2ls7ao75v0t38")

# Language config
app.config["LANGUAGES"] = {
    'en': 'English',
    'ru': 'Русский'
}
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'ya_lublu_kefir!'
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
babel = Babel(app)
SESSION_TYPE = 'redis'
Session(app)

# Blueprints
web_interface = Blueprint('web_interface', __name__)
auth = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.init_app(app)
app.config['TRAP_HTTP_EXCEPTIONS'] = True


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html',
                           code=404,
                           description_1=lazy_gettext("It's kinda empty here.."),
                           description_2=error,
                           show_language=False), 404


@app.errorhandler(500)
def internal_error(error):
    db_sess = db_session.create_session()
    db_sess.rollback()
    return render_template('error.html',
                           code=500,
                           description_1=lazy_gettext("Whoops! Something went wrong!"),
                           description_2=error,
                           show_language=False), 500


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@babel.localeselector
def get_locale():
    if flask.session.get('lang_code', None) is None:
        flask.session['lang_code'] = request.accept_languages.best_match(app.config['LANGUAGES'])
    return flask.session['lang_code']


@app.before_request
def before():
    args = dict(request.args)
    if args and 'lang_code' in args and args['lang_code'] in ('ru', 'en'):
        flask.session['lang_code'] = args['lang_code']
    elif 'lang_code' not in flask.session:
        flask.session['lang_code'] = request.accept_languages.best_match(app.config['LANGUAGES'])


@web_interface.route("/survey")
def survey():
    form = SurveyForm()
    return render_template("form.html", form=form)


@web_interface.route("/")
def index():
    return render_template("index.html", lang_code="ru")


@web_interface.route("/about")
def about():
    return render_template("about.html")


@auth.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            pass

    return render_template("form.html", form=form, action=url_for("auth.login"))


@web_interface.route("/api-description")
def api_description():
    return render_template('api_description.html')


@auth.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = generate_password_hash(form.password.data, method='sha256')

            db_sess = db_session.create_session()
            user = db_sess.query(User).filter_by(email=email).first()
            if user:
                return render_template("form.html",
                                       form=form,
                                       error='exist')
            new_user = User(email=email,
                            name=name,
                            hashed_password=password)
            db_sess.add(new_user)
            db_sess.commit()

    return render_template("form.html", form=form, action=url_for('auth.register'))


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
    # Adding blueprints
    app.register_blueprint(web_interface)
    app.register_blueprint(auth)

    # Running app
    app.run()
