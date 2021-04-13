from os import environ
from flask import Flask, request, render_template, Blueprint, url_for
from werkzeug.utils import redirect
from Blueprints.web_interface import web_interface
from Blueprints.auth import auth
from Blueprints.api import api
from data.users import User
from config import env_setup
import flask
from flask_login import LoginManager
from data import db_session
from flask_babel import Babel, lazy_gettext
from flask_session import Session

env_setup()

app = Flask(__name__)
db_session.global_init(environ.get("DATABASE_URL", ""))

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


login_manager = LoginManager()
login_manager.init_app(app)
app.config['TRAP_HTTP_EXCEPTIONS'] = True


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html',
                           code=404,
                           description_1=lazy_gettext("It's kinda empty here.."),
                           show_language=False,
                           title="Oops.."), 404


@app.errorhandler(500)
def internal_error(error):
    db_sess = db_session.create_session()
    db_sess.rollback()
    return render_template('error.html',
                           code=500,
                           description_1=lazy_gettext("Whoops! Something went wrong!"),
                           show_language=False,
                           title="Oops.."), 500


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


@login_manager.unauthorized_handler
def handle_needs_login():
    return redirect(url_for('auth.login', next=url_for(request.endpoint)))


if __name__ == "__main__":
    # Adding blueprints
    app.register_blueprint(web_interface)
    app.register_blueprint(auth)
    app.register_blueprint(api)

    # Running app
    app.run()
