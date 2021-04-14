from flask import Blueprint, url_for, request, render_template
from flask_babel import lazy_gettext
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from data.users import User
from forms.registration_form import RegistrationForm
from data import db_session

from forms.login_form import LoginForm

auth = Blueprint('auth', __name__)


def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
    except:
        return redirect(fallback)
    return redirect(dest_url)


@auth.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('web_interface.generation_handler'))
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
                                       error='exist', title=lazy_gettext("Registration"))
            new_user = User(email=email,
                            name=name,
                            hashed_password=password)
            db_sess.add(new_user)
            db_sess.commit()

    return render_template("form.html", form=form, action=url_for('auth.register'), title=lazy_gettext("Registration"))


@auth.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('web_interface.generation_handler'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            email = request.form.get('email')
            password = request.form.get('password')
            user = db_sess.query(User).filter_by(email=email).first()
            if user is None or not check_password_hash(user.hashed_password, password):
                return render_template("form.html", form=form,
                                action=url_for('auth.login', next=request.endpoint),
                                title=lazy_gettext("Login"),
                                error=lazy_gettext("Wrong credentials data"))
            login_user(user, remember=True)
            return redirect_dest("/generate")
    k = {}
    if request.endpoint != "auth.login":
        k["next"] = request.endpoint
    return render_template("form.html", form=form,
                           action=url_for('auth.login', **k),
                           title=lazy_gettext("Login"))


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("web_interface.index"))
