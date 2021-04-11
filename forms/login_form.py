from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    form_name = lazy_gettext(u'Sign in')
    email = EmailField(lazy_gettext(u'Email'), validators=[DataRequired()], )
    password = PasswordField(lazy_gettext(u'Password'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext(u'Login'))
