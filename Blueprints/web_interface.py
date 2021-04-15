from flask import Blueprint, render_template, request, url_for
from flask_babel import lazy_gettext
from flask_login import login_required, current_user
from names_generator import generate_name

from forms.survey import SurveyForm

from drawing.colors import color_palette
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data.db_session import create_session
from data.project import Project

from data.design import Design

web_interface = Blueprint('web_interface', __name__)


@web_interface.route("/survey")
@login_required
def survey():
    form = SurveyForm()
    return render_template("form.html", form=form, title=lazy_gettext("Survey"))


@web_interface.route("/")
def index():
    return render_template("meta/index.html", lang_code="ru", title=lazy_gettext("Neural Designer"))


@web_interface.route("/about")
def about():
    return render_template("meta/about.html", title=lazy_gettext("About us"))


@web_interface.route("/api-description")
def api_description():
    return render_template('meta/api_description.html', title=lazy_gettext("API Description"))


@web_interface.route("/generate")
@login_required
def generation_handler():
    return render_template("design/logo_generation.html", title=lazy_gettext("Generate"))


@web_interface.route('/palettes')
@login_required
def palettes():
    palette = color_palette()
    colors = list(map(lambda x: f'rgb({x[0]}, {x[1]}, {x[2]})', palette))
    return '\n'.join(map(lambda x: f"<p style='background-color:{x}'>||||||||</p>", colors)) + f'\n{palette}'


@web_interface.route("/me")
@login_required
def me():
    return render_template("meta/me.html", title=current_user.name)


@web_interface.route("/projects")
def projects_view():
    return render_template("project/projects.html", title="Projects")


@web_interface.route("/projects/<string:name>")
@login_required
def project_view(name):
    p = current_user.get_project(name)
    if p is not None:
        return render_template("project/project.html", title=name, show_language=False, project=p)
    return abort(404)


@web_interface.route("/projects/<string:name>/create-design", methods=['GET', 'POST'])
@login_required
def design_creation_handler(name):
    p = current_user.get_project(name)
    if p is not None:
        if request.method == 'GET':
            return render_template("design/design.html", title=name, show_language=False, project=p)
        if request.method == 'POST':
            svg_string = request.json.get('svg')
            if svg_string is not None:
                db_sess = create_session()
                d = Design(svg_string, p)
                db_sess.add(d)
                db_sess.commit()
                return "Success", 200
            return abort(400)
    return abort(404)


@web_interface.route("/create-project")
@login_required
def project_creation_handler():
    project_name = generate_name(style="hyphen")
    while current_user.get_project(project_name) is not None:
        project_name = generate_name(style="hyphen")
    db_sess = create_session()
    p = Project(project_name, current_user)
    db_sess.add(p)
    db_sess.commit()
    db_sess.close()
    return redirect(url_for("web_interface.project_view", name=project_name))


@web_interface.route("/fonts")
def fonts_view():
    return render_template("fonts/fonts.html", title="Fonts")


@web_interface.route("/create-font")
def font_creation_handler():
    return render_template("fonts/create_font.html", title="New font")
