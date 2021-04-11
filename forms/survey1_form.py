from flask import g
from flask_babel import gettext, lazy_gettext
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired


class SurveyForm(FlaskForm):
    name = StringField(lazy_gettext(u'What is your name?'), validators=[DataRequired()])
    squad_id = IntegerField(lazy_gettext(u'Which squad are you from?'), validators=[DataRequired()])
    q1 = StringField(lazy_gettext(u'Which advertisments do ypu like?'), validators=[DataRequired()])
    q2 = IntegerField(lazy_gettext(u'Where are you from?'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext(u'Send'))
