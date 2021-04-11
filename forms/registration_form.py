from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length


class RegistrationForm(FlaskForm):
    form_name = lazy_gettext(u'Sign up')
    name = StringField(lazy_gettext(u'Name'), validators=[DataRequired()])
    email = EmailField(lazy_gettext(u'Email'), validators=[DataRequired()])
    password = PasswordField(lazy_gettext(u'Password'), validators=[DataRequired(), Length(8)])
    submit = SubmitField(lazy_gettext(u'Register'))
