from flask import Blueprint, render_template
from flask_babel import lazy_gettext
from flask_login import login_required

from forms.survey1_form import SurveyForm

from drawing.colors import color_palette

web_interface = Blueprint('web_interface', __name__)


@web_interface.route("/survey")
@login_required
def survey():
    form = SurveyForm()
    return render_template("form.html", form=form, title=lazy_gettext("Survey"))


@web_interface.route("/")
def index():
    return render_template("index.html", lang_code="ru", title=lazy_gettext("Neural Designer"))


@web_interface.route("/about")
def about():
    return render_template("about.html", title=lazy_gettext("About us"))


@web_interface.route("/api-description")
def api_description():
    return render_template('api_description.html', title=lazy_gettext("API Description"))


@web_interface.route("/generate")
@login_required
def generation_handler():
    return render_template("logo_generation.html", title=lazy_gettext("Generate"))


@web_interface.route('/palettes')
@login_required
def palettes():
    palette = color_palette()
    colors = list(map(lambda x: f'rgb({x[0]}, {x[1]}, {x[2]})', palette))
    return '\n'.join(map(lambda x: f"<p style='background-color:{x}'>||||||||</p>", colors)) + f'\n{palette}'


@web_interface.route("/me")
@login_required
def me():
    return render_template("me.html")
